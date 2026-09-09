"""
Event Bus & Notification Dispatcher for Real-Time Execution Streaming and Updates.
"""

from typing import Callable, Dict, List, Any
import threading

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, payload: Dict[str, Any]):
        with self._lock:
            callbacks = list(self._subscribers.get(event_type, []))
        
        for cb in callbacks:
            try:
                cb(payload)
            except Exception:
                pass

event_bus = EventBus()
