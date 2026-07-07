"""
Nova AI Desktop Assistant
-------------------------

Thread Manager

Centralized thread management for the UI layer.

Responsibilities
----------------
- Execute background tasks
- Keep UI responsive
- Deliver results safely to the GUI thread
- Manage thread lifecycle
- Gracefully shutdown workers
"""

from __future__ import annotations

import logging
import traceback
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import (
    QObject,
    QRunnable,
    QThreadPool,
    Signal,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Worker Signals
# ==========================================================

class WorkerSignals(QObject):
    """
    Signals emitted by background workers.
    """

    started = Signal()

    finished = Signal()

    result = Signal(object)

    error = Signal(str)

    progress = Signal(int)


# ==========================================================
# Worker
# ==========================================================

class Worker(QRunnable):
    """
    Generic background worker.
    """

    def __init__(
        self,
        function: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__()

        self.function = function

        self.args = args

        self.kwargs = kwargs

        self.signals = WorkerSignals()

        self.setAutoDelete(True)

    def run(self) -> None:
        """
        Execute the worker task.
        """

        self.signals.started.emit()

        try:
            result = self.function(
                *self.args,
                **self.kwargs,
            )

            self.signals.result.emit(result)

        except Exception:

            logger.exception(
                "Worker execution failed."
            )

            self.signals.error.emit(
                traceback.format_exc()
            )

        finally:

            self.signals.finished.emit()


# ==========================================================
# Thread Manager
# ==========================================================

class ThreadManager(QObject):
    """
    Singleton wrapper around Qt's global thread pool.
    """

    task_started = Signal()

    task_finished = Signal()

    def __init__(self) -> None:
        super().__init__()

        self._pool = QThreadPool.globalInstance()

        self._pool.setExpiryTimeout(30_000)

        self._pool.setMaxThreadCount(
            self._pool.maxThreadCount()
        )

    @property
    def pool(self) -> QThreadPool:
        return self._pool

    @property
    def max_thread_count(self) -> int:
        return self._pool.maxThreadCount()

    @property
    def active_thread_count(self) -> int:
        return self._pool.activeThreadCount()

    def submit(
        self,
        function: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Worker:
        """
        Submit a task to the global thread pool.
        """

        worker = Worker(
            function,
            *args,
            **kwargs,
        )

        worker.signals.started.connect(
            self.task_started
        )

        worker.signals.finished.connect(
            self.task_finished
        )

        self._pool.start(worker)

        return worker

    def submit_with_callbacks(
        self,
        function: Callable[..., Any],
        *args: Any,
        on_result: Callable[[Any], None] | None = None,
        on_error: Callable[[str], None] | None = None,
        on_finished: Callable[[], None] | None = None,
        on_progress: Callable[[int], None] | None = None,
        **kwargs: Any,
    ) -> Worker:
        """
        Submit a task with optional callbacks.
        """

        worker = self.submit(function, *args, **kwargs)

        if on_result is not None:
            worker.signals.result.connect(on_result)

        if on_error is not None:
            worker.signals.error.connect(on_error)

        if on_finished is not None:
            worker.signals.finished.connect(on_finished)

        if on_progress is not None:
            worker.signals.progress.connect(on_progress)

        return worker

    def clear(self) -> None:
        """
        Clear pending tasks that have not yet started.
        """

        self._pool.clear()

    def wait_for_done(
        self,
        timeout: int = -1,
    ) -> bool:
        """
        Wait for all running workers to finish.

        Parameters
        ----------
        timeout:
            Timeout in milliseconds.
            -1 waits indefinitely.
        """

        return self._pool.waitForDone(timeout)

    def set_max_thread_count(
        self,
        count: int,
    ) -> None:
        """
        Set the maximum number of concurrent worker threads.
        """

        if count < 1:
            raise ValueError(
                "Thread count must be greater than zero."
            )

        self._pool.setMaxThreadCount(count)

    def contains_running_tasks(self) -> bool:
        """
        Returns True if one or more workers are active.
        """

        return self.active_thread_count > 0

    def shutdown(
        self,
        timeout: int = 5000,
    ) -> bool:
        """
        Gracefully shut down the thread pool.
        """

        self.clear()

        return self.wait_for_done(timeout)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"active={self.active_thread_count}, "
            f"max={self.max_thread_count})"
        )


# ==========================================================
# Singleton
# ==========================================================

thread_manager = ThreadManager()


def get_thread_manager() -> ThreadManager:
    """
    Return the global ThreadManager instance.
    """

    return thread_manager


__all__ = [
    "WorkerSignals",
    "Worker",
    "ThreadManager",
    "thread_manager",
    "get_thread_manager",
]