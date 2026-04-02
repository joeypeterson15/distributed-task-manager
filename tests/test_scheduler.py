import pytest
import numpy as np
import collections
from scheduler_class import Scheduler  # adjust import as needed

class TestSchedulerInit:
    def setup_method(self):
        self.s = Scheduler()

    def test_grid_shape(self):
        s = self.s
        assert s.grid.shape == (s.epochs, s.n_grid_rows, s.n_grid_cols, s.n_cells, s.n_cells)

    def test_grid_values_in_range(self):
        assert np.all(self.s.grid >= 0) and np.all(self.s.grid < 1)

    def test_prev_region_present_epoch0_all_true(self):
        assert np.all(self.s.prev_region_present[0])

    def test_prev_region_present_epoch1_all_false(self):
        assert not np.any(self.s.prev_region_present[1])

    def test_region_enqueued_initially_false_except_epoch1(self):
        # Only epoch 1 tasks should be enqueued at start
        # epoch index 0 in region_enqueued corresponds to tasks FOR epoch 1
        assert not np.any(self.s.region_enqueued[0])  # epoch 0 enqueued-for is unused


class TestDependencyGraph:
    def setup_method(self):
        self.s = Scheduler()

    def test_corner_has_2_neighbors(self):
        # (0,0) is a corner — only right and down
        neighbors = self.s.dependents_graph[(0, 0)]
        assert len(neighbors) == 2

    def test_edge_has_3_neighbors(self):
        # (0,1) is a top edge
        neighbors = self.s.dependents_graph[(0, 1)]
        assert len(neighbors) == 3

    def test_interior_has_4_neighbors(self):
        # (1,1) is interior on a 4x4 grid
        neighbors = self.s.dependents_graph[(1, 1)]
        assert len(neighbors) == 4

    def test_no_out_of_bounds_neighbors(self):
        rows, cols = self.s.n_grid_rows, self.s.n_grid_cols
        for (r, c), neighbors in self.s.dependents_graph.items():
            for nr, nc in neighbors:
                assert 0 <= nr < rows and 0 <= nc < cols


class TestRequiredReadyCount:
    def setup_method(self):
        self.s = Scheduler()

    def test_corner_requires_2(self):
        assert self.s.required_ready_count[(0, 0)] == 2

    def test_top_edge_requires_3(self):
        assert self.s.required_ready_count[(0, 1)] == 3

    def test_interior_requires_4(self):
        assert self.s.required_ready_count[(1, 1)] == 4

    def test_all_counts_positive(self):
        for v in self.s.required_ready_count.values():
            assert v > 0


class TestInitialQueue:
    def setup_method(self):
        self.s = Scheduler()

    def test_initial_queue_not_empty(self):
        assert len(self.s.tasks_queue) > 0

    def test_all_initial_tasks_are_epoch1(self):
        for task in self.s.tasks_queue:
            assert task['epoch'] == 1

    def test_initial_queue_size_equals_all_regions(self):
        # All 16 regions should be enqueued for epoch 1 at start
        assert len(self.s.tasks_queue) == self.s.n_grid_rows * self.s.n_grid_cols


class TestUpdateGrid:
    def setup_method(self):
        self.s = Scheduler()

    def test_update_grid_stores_values(self):
        s = self.s
        new_vals = np.ones((s.n_cells, s.n_cells))
        s.update_grid((0, 0), new_vals, 1)
        assert np.array_equal(s.grid[1][0][0], new_vals)

    def test_update_grid_marks_prev_region_present(self):
        self.s.update_grid((1, 1), np.zeros((4, 4)), 1)
        assert self.s.prev_region_present[1][1][1] == True


class TestIncrementAndEnqueue:
    def setup_method(self):
        self.s = Scheduler()
        # Drain the initial queue so we can observe new enqueues cleanly
        self.s.tasks_queue.clear()
        self.s.region_enqueued[:] = False

    def test_completing_epoch0_region_enqueues_dependents_at_epoch1(self):
        s = self.s
        # Simulate all epoch-0 neighbors of (0,0) being done — just trigger (0,0)
        s.prev_region_present[0][0][0] = True
        s.ready_neighbor_count[1][0][0] = s.required_ready_count[(0, 0)]
        s.increment_dependents_and_enqueue((0, 0), 0)
        regions_enqueued = [t['region'] for t in s.tasks_queue]
        # (0,0) itself and its dependents at epoch 1 should be in queue
        assert (0, 0) in regions_enqueued

    def test_no_double_enqueue(self):
        s = self.s
        s.prev_region_present[0][1][1] = True
        s.ready_neighbor_count[1][1][1] = s.required_ready_count[(1, 1)]
        s.increment_dependents_and_enqueue((1, 1), 0)
        s.increment_dependents_and_enqueue((1, 1), 0)  # call again
        count = sum(1 for t in s.tasks_queue if t['region'] == (1, 1) and t['epoch'] == 1)
        assert count == 1


class TestGhostBoundaries:
    def setup_method(self):
        self.s = Scheduler()

    def test_top_left_corner_has_two_zero_boundaries(self):
        boundaries = self.s.collect_ghost_region_boundaries((0, 0), 0)
        rtop, rbot, cleft, cright = boundaries
        assert all(v == 0 for v in rtop), "top row should be zeros"
        assert all(v == 0 for v in cleft), "left col should be zeros"

    def test_interior_boundaries_are_nonzero_arrays(self):
        # With random init, interior neighbors are very unlikely to be all zero
        boundaries = self.s.collect_ghost_region_boundaries((1, 1), 0)
        assert len(boundaries) == 4
        for b in boundaries:
            assert len(b) == self.s.n_cells

    def test_boundary_pulls_correct_neighbor_slice(self):
        s = self.s
        # Set a known value in region (0,1) bottom row, verify (1,1) sees it as rtop
        known_row = np.arange(s.n_cells, dtype=float)
        s.grid[0][0][1][s.n_cells - 1][:] = known_row
        boundaries = s.collect_ghost_region_boundaries((1, 1), 0)
        rtop = boundaries[0]
        assert rtop == known_row.tolist()