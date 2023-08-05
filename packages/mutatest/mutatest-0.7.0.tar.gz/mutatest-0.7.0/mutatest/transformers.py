"""AST Transformers.
"""
import ast
import logging

from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Set, Union


LOGGER = logging.getLogger(__name__)


class LocIndex(NamedTuple):
    """Location index within AST to mark mutatest targets."""

    ast_class: str
    lineno: int
    col_offset: int
    op_type: Any  # varies based on the visit_Node definition in MutateAST


class MutationOpSet(NamedTuple):
    """Container for compatible mutation operations. Also used in the CLI display."""

    name: str
    desc: str
    operations: Set[Any]


class MutateAST(ast.NodeTransformer):
    """AST NodeTransformer to replace nodes with mutations by visits."""

    def __init__(
        self,
        target_idx: Optional[LocIndex] = None,
        mutation: Optional[Any] = None,
        readonly: bool = False,
        src_file: Optional[Union[Path, str]] = None,
    ) -> None:
        """Create the AST node transformer for mutations.

        If readonly is set to None then no transformations are applied;
        however, the locs attribute is updated with the locations of nodes that could
        be transformed. This allows the class to function both as an inspection method
        and as a mutatest transformer.

        Note that different nodes hand the LocIndex differently based on the context. For
        example, visit_BinOp uses direct AST types, while visit_NameConstant uses values,
        and visit_AugAssign uses custom strings in a dictionary mapping.

        Args:
            target_idx: Location index for the mutatest in the AST
            mutation: the mutatest to apply, may be a type or a value
            readonly: flag for read-only operations, used to visit nodes instead of transform
            src_file: Source file name, used for logging purposes
        """
        self.locs: Set[LocIndex] = set()

        # managed via @property
        self._target_idx = target_idx
        self._mutation = mutation
        self._readonly = readonly
        self._src_file = src_file

    @property
    def target_idx(self) -> Optional[LocIndex]:
        """target_idx: Location index for the mutatest in the AST"""
        return self._target_idx

    @property
    def mutation(self) -> Optional[Any]:
        """mutation: the mutatest to apply, may be a type or a value"""
        return self._mutation

    @property
    def readonly(self) -> bool:
        """readonly: flag for read-only operations, used to visit nodes instead of transform"""
        return self._readonly

    @property
    def src_file(self) -> Optional[Union[Path, str]]:
        """src_file: Source file name, used for logging purposes"""
        return self._src_file

    def visit_AugAssign(self, node: ast.AugAssign) -> ast.AST:
        """AugAssign is -=, +=, /=, *= for augmented assignment."""
        self.generic_visit(node)
        log_header = f"visit_AugAssign: {self.src_file}:"

        # custom mapping of string keys to ast operations that can be used
        # in the nodes since these overlap with BinOp types
        aug_mappings = {
            "AugAssign_Add": ast.Add,
            "AugAssign_Sub": ast.Sub,
            "AugAssign_Mult": ast.Mult,
            "AugAssign_Div": ast.Div,
        }

        rev_mappings = {v: k for k, v in aug_mappings.items()}
        idx_op = rev_mappings.get(type(node.op), None)

        # edge case protection in case the mapping isn't known for substitution
        # in that instance, return the node and take no action
        if not idx_op:
            LOGGER.debug(
                "%s (%s, %s): unknown aug_assignment: %s",
                log_header,
                node.lineno,
                node.col_offset,
                type(node.op),
            )
            return node

        idx = LocIndex("AugAssign", node.lineno, node.col_offset, idx_op)
        self.locs.add(idx)

        if idx == self.target_idx and self.mutation in aug_mappings and not self.readonly:
            LOGGER.debug("%s mutating idx: %s with %s", log_header, self.target_idx, self.mutation)
            return ast.copy_location(
                ast.AugAssign(
                    target=node.target,
                    op=aug_mappings[self.mutation](),  # awkward syntax to call type from mapping
                    value=node.value,
                ),
                node,
            )

        LOGGER.debug("%s (%s, %s): no mutations applied.", log_header, node.lineno, node.col_offset)
        return node

    def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
        """BinOp nodes are bit-shifts and general operators like add, divide, etc."""
        self.generic_visit(node)
        log_header = f"visit_BinOp: {self.src_file}:"

        idx = LocIndex("BinOp", node.lineno, node.col_offset, type(node.op))
        self.locs.add(idx)

        if idx == self.target_idx and self.mutation and not self.readonly:
            LOGGER.debug("%s mutating idx: %s with %s", log_header, self.target_idx, self.mutation)
            return ast.copy_location(
                ast.BinOp(left=node.left, op=self.mutation(), right=node.right), node
            )

        LOGGER.debug("%s (%s, %s): no mutations applied.", log_header, node.lineno, node.col_offset)
        return node

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.AST:
        """Boolean operations, AND/OR."""
        self.generic_visit(node)
        log_header = f"visit_BoolOp: {self.src_file}:"

        idx = LocIndex("BoolOp", node.lineno, node.col_offset, type(node.op))
        self.locs.add(idx)

        if idx == self.target_idx and self.mutation and not self.readonly:
            LOGGER.debug("%s mutating idx: %s with %s", log_header, self.target_idx, self.mutation)
            return ast.copy_location(ast.BoolOp(op=self.mutation(), values=node.values), node)

        LOGGER.debug("%s (%s, %s): no mutations applied.", log_header, node.lineno, node.col_offset)
        return node

    def visit_Compare(self, node: ast.Compare) -> ast.AST:
        """Compare nodes are ==, >= etc."""
        self.generic_visit(node)
        log_header = f"visit_Compare: {self.src_file}:"

        # taking only the first operation in the compare node
        # in basic testing, things like (a==b)==1 still end up with lists of 1,
        # but since the AST docs specify a list of operations this seems safer.
        idx = LocIndex("Compare", node.lineno, node.col_offset, type(node.ops[0]))
        self.locs.add(idx)

        if idx == self.target_idx and self.mutation and not self.readonly:
            LOGGER.debug("%s mutating idx: %s with %s", log_header, self.target_idx, self.mutation)

            # TODO: Determine when/how this case would actually be called
            if len(node.ops) > 1:
                # unlikely test case where the comparison has multiple values
                LOGGER.debug("%s multiple compare ops in node, len: %s", log_header, len(node.ops))
                existing_ops = [i for i in node.ops]
                mutation_ops = [self.mutation()] + existing_ops[1:]

                return ast.copy_location(
                    ast.Compare(left=node.left, ops=mutation_ops, comparators=node.comparators),
                    node,
                )

            else:
                # typical comparison case, will also catch (a==b)==1 as an example.
                LOGGER.debug("%s single comparison node operation", log_header)
                new_node = ast.Compare(
                    left=node.left, ops=[self.mutation()], comparators=node.comparators
                )
                LOGGER.debug("%s new node:\n%s", log_header, ast.dump(new_node))

                return ast.copy_location(
                    ast.Compare(
                        left=node.left, ops=[self.mutation()], comparators=node.comparators
                    ),
                    node,
                )

        LOGGER.debug("%s (%s, %s): no mutations applied.", log_header, node.lineno, node.col_offset)
        return node

    def visit_Index(self, node: ast.Index) -> ast.AST:
        """Index visit e.g. i[0], i[0][1]."""
        self.generic_visit(node)
        log_header = f"visit_Index: {self.src_file}:"

        # Index Node has a value attribute that can be either Num node or UnaryOp node
        # depending on whether the value is positive or negative.
        n_value = node.value
        idx = None

        index_mutations = {
            "Index_NumZero": ast.Num(n=0),
            "Index_NumPos": ast.Num(n=1),
            "Index_NumNeg": ast.UnaryOp(op=ast.USub(), operand=ast.Num(n=1)),
        }

        # index is a non-negative number e.g. i[0], i[1]
        if isinstance(n_value, ast.Num):
            # positive integer case
            if n_value.n != 0:
                idx = LocIndex("Index_NumPos", n_value.lineno, n_value.col_offset, "Index_NumPos")
                self.locs.add(idx)

            # zero value case
            else:
                idx = LocIndex("Index_NumZero", n_value.lineno, n_value.col_offset, "Index_NumZero")
                self.locs.add(idx)

        # index is a negative number e.g. i[-1]
        if isinstance(n_value, ast.UnaryOp):
            idx = LocIndex("Index_NumNeg", n_value.lineno, n_value.col_offset, "Index_NumNeg")
            self.locs.add(idx)

        if idx == self.target_idx and self.mutation and not self.readonly:
            LOGGER.debug("%s mutating idx: %s with %s", log_header, self.target_idx, self.mutation)
            mutation = index_mutations[self.mutation]

            # uses AST.fix_missing_locations since the values of ast.Num and  ast.UnaryOp also need
            # lineno and col-offset values. This is a recursive fix.
            return ast.fix_missing_locations(ast.copy_location(ast.Index(value=mutation), node))

        LOGGER.debug(
            "%s (%s, %s): no mutations applied.", log_header, n_value.lineno, n_value.col_offset
        )
        return node

    def visit_NameConstant(self, node: ast.NameConstant) -> ast.AST:
        """NameConstants: True/False/None."""
        self.generic_visit(node)
        log_header = f"visit_NameConstant: {self.src_file}:"

        idx = LocIndex("NameConstant", node.lineno, node.col_offset, node.value)
        self.locs.add(idx)

        if idx == self.target_idx and not self.readonly:
            LOGGER.debug("%s mutating idx: %s with %s", log_header, self.target_idx, self.mutation)
            return ast.copy_location(ast.NameConstant(value=self.mutation), node)

        LOGGER.debug("%s (%s, %s): no mutations applied.", log_header, node.lineno, node.col_offset)
        return node

    def visit_Subscript(self, node: ast.Subscript) -> ast.AST:
        """Subscript slice operations.g. x[1:] or y[::2]"""
        self.generic_visit(node)
        log_header = f"visit_Subscript: {self.src_file}:"
        idx = None

        # Subscripts have slice properties with col/lineno, slice itself does not have line/col
        # Index is also a valid Subscript slice property
        slice = node.slice
        if not isinstance(slice, ast.Slice):
            LOGGER.debug("%s (%s, %s): not a slice node.", log_header, node.lineno, node.col_offset)
            return node

        # Built "on the fly" based on the various conditions for operation types
        slice_mutations: Dict[str, ast.Slice] = {}

        # NONE Swap Operation
        # upper slice range e.g. x[:2] will become x[2:]
        if slice.lower is None and slice.upper is not None:
            idx = LocIndex("Slice_SwapNoneUL", node.lineno, node.col_offset, "Slice_SwapNoneUL")
            slice_mutations["Slice_SwapNoneUL"] = ast.Slice(
                lower=slice.upper, upper=None, step=slice.step
            )

            self.locs.add(idx)

        # lower slice range e.g. x[1:] will become x[:1]
        if slice.upper is None and slice.lower is not None:
            idx = LocIndex("Slice_SwapNoneLU", node.lineno, node.col_offset, "Slice_SwapNoneLU")
            slice_mutations["Slice_SwapNoneLU"] = ast.Slice(
                lower=None, upper=slice.lower, step=slice.step
            )
            self.locs.add(idx)

        # Shrink Operation
        # range shrink e.g. x[2,4] becomes x[2,3]
        # More likely to generate useful mutants than increasing the range
        if slice.lower is not None and slice.upper is not None:
            if isinstance(slice.upper, ast.Num):
                idx = LocIndex("Slice_UPosToZero", node.lineno, node.col_offset, "Slice_UPosToZero")
                slice_mutations["Slice_UPosToZero"] = ast.Slice(
                    lower=slice.lower, upper=ast.Num(n=slice.upper.n - 1), step=slice.step
                )
                LOGGER.debug("UPosToZero: %s", ast.dump(slice_mutations["Slice_UPosToZero"]))
                self.locs.add(idx)

            if isinstance(slice.upper, ast.UnaryOp):
                idx = LocIndex("Slice_UNegToZero", node.lineno, node.col_offset, "Slice_UNegToZero")

                slice_mutations["Slice_UNegToZero"] = ast.Slice(
                    lower=slice.lower,
                    upper=ast.UnaryOp(
                        op=ast.USub(), operand=ast.Num(n=slice.upper.operand.n - 1)  # type: ignore
                    ),
                    step=slice.step,
                )
                LOGGER.debug("UNegToZero: %s", ast.dump(slice_mutations["Slice_UNegToZero"]))

                self.locs.add(idx)

        # Apply Mutation
        if idx == self.target_idx and not self.readonly:
            LOGGER.debug("%s mutating idx: %s with %s", log_header, self.target_idx, self.mutation)
            mutation = slice_mutations[str(self.mutation)]  # self.mutation should be string already
            # uses AST.fix_missing_locations since the values of ast.Num and  ast.UnaryOp also need
            # lineno and col-offset values. This is a recursive fix.
            return ast.fix_missing_locations(
                ast.copy_location(
                    ast.Subscript(value=node.value, slice=mutation, ctx=node.ctx), node
                )
            )

        LOGGER.debug("%s (%s, %s): no mutations applied.", log_header, node.lineno, node.col_offset)
        return node


def get_compatible_operation_sets() -> List[MutationOpSet]:
    """Utility function to return a list of compatible AST mutations with names.

    All of the mutation transformation sets that are supported by mutatest are defined here.
    See: https://docs.python.org/3/library/ast.html#abstract-grammar

    This is used to create the search space in finding mutations for a target, and
    also to list the support operations in the CLI help function.

    Returns:
        List of MutationOpSets that have substitutable operations
    """

    # AST operations that are sensible mutations for each other
    binop_types: Set[type] = {ast.Add, ast.Sub, ast.Div, ast.Mult, ast.Pow, ast.Mod, ast.FloorDiv}
    binop_bit_cmp_types: Set[type] = {ast.BitAnd, ast.BitOr, ast.BitXor}
    binop_bit_shift_types: Set[type] = {ast.LShift, ast.RShift}
    cmpop_types: Set[type] = {ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE}
    cmpop_is_types: Set[type] = {ast.Is, ast.IsNot}
    cmpop_in_types: Set[type] = {ast.In, ast.NotIn}
    boolop_types: Set[type] = {ast.And, ast.Or}

    # Python built-in constants (singletons) that can be used with NameConstant AST node
    named_const_singletons: Set[Union[bool, None]] = {True, False, None}

    # Custom augmentation ops to differentiate from bin_op types
    # these are defined for substitution within the visit_AugAssign node and need to match
    aug_assigns: Set[str] = {"AugAssign_Add", "AugAssign_Sub", "AugAssign_Mult", "AugAssign_Div"}

    # Custom references for substitutions of zero, positive, and negative iterable indicies
    index_types: Set[str] = {"Index_NumPos", "Index_NumNeg", "Index_NumZero"}

    # Custom references for subscript substitutions for slice mutations
    slice_types: Set[str] = {
        "Slice_SwapNoneLU",
        "Slice_SwapNoneUL",
        "Slice_UPosToZero",
        "Slice_UNegToZero",
    }

    return [
        MutationOpSet(
            name="AugAssign", desc="Augmented assignment e.g. += -= /= *=", operations=aug_assigns
        ),
        MutationOpSet(
            name="BinOp", desc="Binary operations e.g. + - * / %", operations=binop_types
        ),
        MutationOpSet(
            name="BinOp Bit Comparison",
            desc="Bitwise comparison operations e.g. x & y, x | y, x ^ y",
            operations=binop_bit_cmp_types,
        ),
        MutationOpSet(
            name="BinOp Bit Shifts",
            desc="Bitwise shift operations e.g. << >>",
            operations=binop_bit_shift_types,
        ),
        MutationOpSet(
            name="BoolOp", desc="Boolean operations e.g. and or", operations=boolop_types
        ),
        MutationOpSet(
            name="Compare", desc="Comparison operations e.g. == >= <= > <", operations=cmpop_types
        ),
        MutationOpSet(
            name="Compare In", desc="Compare membership e.g. in, not in", operations=cmpop_in_types
        ),
        MutationOpSet(
            name="Compare Is", desc="Comapre identity e.g. is, is not", operations=cmpop_is_types
        ),
        MutationOpSet(
            name="Index",
            desc="Index values for iterables e.g. i[-1], i[0], i[0][1]",
            operations=index_types,
        ),
        MutationOpSet(
            name="NameConstant",
            desc="Named constant mutations e.g. True, False, None",
            operations=named_const_singletons,
        ),
        MutationOpSet(
            name="Slices",
            desc=(
                "Slice mutations to swap lower/upper values, or change range e.g. x[2:] to x[:2],"
                " or x[1:5] to x[1:4]"
            ),
            operations=slice_types,
        ),
    ]


def get_mutations_for_target(target: LocIndex) -> Set[Any]:
    """Given a target, find all the mutations that could apply from the AST definitions.

    Args:
        target: the location index target

    Returns:
        Set of types that can mutated into the target op
    """
    search_space: List[Set[Any]] = [m.operations for m in get_compatible_operation_sets()]
    mutation_ops: Set[Any] = set()

    for potential_ops in search_space:
        if target.op_type in potential_ops:
            LOGGER.debug("Potential mutatest operations found for target: %s", target.op_type)
            mutation_ops = potential_ops.copy()
            mutation_ops.remove(target.op_type)

            # Special case where Slice-Ops are self-referential, and are set to self
            if isinstance(target.op_type, str) and target.op_type.startswith("Slice_"):
                mutation_ops = {target.op_type}

            break

    return mutation_ops


def get_ast_from_src(src_file: Union[str, Path]) -> ast.Module:
    """Create an AST from a source file

    Args:
        src_file: the source file to  build into an AST

    Returns:
        The AST
    """
    with open(src_file, "rb") as src_stream:
        source = src_stream.read()
        return ast.parse(source)
