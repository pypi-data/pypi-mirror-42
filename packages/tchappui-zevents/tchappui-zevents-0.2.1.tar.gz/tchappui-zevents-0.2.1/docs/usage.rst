=====
Usage
=====

To use zevents in a project::

    import zevents

The zevents package defines two standard events that can be used to control an
event-driven application: TickEvent and QuitEvent. TickEvent aims at being sent
in the main application loop to process queues in the internal event manager.

Here is an example of how to use those events to control an echo console
application using an event-based logic.

The KeyboardController class subscribes to Tick events, reacts to those by
asking the user to enter a few words and sends a Quit event if the user inputs
a `\\q`::

    from zevents.events import TickEvent, QuitEvent
    from zevents.dispatch import listener, handler

    @listener
    class KeyboardController:
        """Controller responsible to handle keyboard events."""

        # Available actions
        actions = {
            "\\q": QuitEvent.send,
        }

        @handler(TickEvent)
        def _on_tick(self, event):
            """Handles the Tick events."""
            user = input("Say something or enter \q to quit: ")
            action = self.actions.get(
                user.lower().strip(), lambda: print(user)
            )
            action()

The EchoApplication class could be written as follows::

    from zevents.events import TickEvent, QuitEvent
    from zevents.dispatch import listener, handler

    @listener
    class EchoApplication:
        """Represents the application itself."""

        def __init__(self):
            self.running = False
            self.controller = KeyboardController()

        @handler(QuitEvent)
        def _on_quit(self, event):
            """Handles Quit events."""
            self.running = False

        def run(self):
            """Starts the application event loop."""
            self.running = True
            while self.running:
                # We send a Tick event in each loop
                TickEvent.send()

Let's run this application::

    >>> app = EchoApplication()
    >>> app.run()

