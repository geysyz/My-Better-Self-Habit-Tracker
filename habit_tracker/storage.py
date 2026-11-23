from abc import ABC, abstractmethod


class HabitStorage(ABC):
    """What HabitTracker needs from storage. Any implementation
    (JSON file, in-memory fake, database) can be swapped in."""

    @abstractmethod
    def load(self):
        """Return a list of Habit objects."""

    @abstractmethod
    def save(self, habits):
        """Persist the given list of Habit objects."""