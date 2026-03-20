#!/usr/bin/env python3
"""
Ulauncher API Compatibility Test Extension

This extension tests various aspects of the Ulauncher v5 Extension API by
rendering different types of items and actions to verify compatibility.
"""

import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesUpdateEvent, SystemExitEvent, PreferencesEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.action.ActionList import ActionList
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

logger = logging.getLogger(__name__)

PAGE_SIZE = 6


def paginate_items(items, page):
    """Return a page of items (PAGE_SIZE per page) with a 'More' item if there are more."""
    start = page * PAGE_SIZE
    page_items = items[start:start + PAGE_SIZE]

    if start + PAGE_SIZE < len(items):
        page_items.append(ExtensionResultItem(
            icon='images/icon.png',
            name=f'More... ({len(items) - start - PAGE_SIZE} remaining)',
            description='Show next page of results',
            on_enter=ExtensionCustomAction(
                {'action': 'next_page', 'page': page + 1},
                keep_app_open=True
            )
        ))

    return RenderResultListAction(page_items)


class APICompatibilityTestExtension(Extension):
    """Main extension class"""

    def __init__(self):
        super().__init__()
        self._cached_items = []
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())
        self.subscribe(SystemExitEvent, SystemExitEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())


class KeywordQueryEventListener(EventListener):
    """Handles keyword query events and returns test items"""

    def on_event(self, event, extension):
        """
        Return a list of items testing different aspects of the API
        """
        logger.info(f"KeywordQueryEvent: query='{event.get_argument()}'")

        query = event.get_argument() or ""
        items = []

        # Test 0: KeywordQueryEvent and Query object methods
        query_obj = event.get_query()
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 0: KeywordQueryEvent & Query methods',
            description=(
                f'event: get_argument={repr(event.get_argument())}, get_keyword={repr(event.get_keyword())}'
                f' | query: get_argument={repr(query_obj.get_argument())}, get_keyword={repr(query_obj.get_keyword())}, is_mode_active={query_obj.is_mode_active()}'
            ),
            on_enter=DoNothingAction()
        ))

        # Test 1: ExtensionResultItem with HideWindowAction
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 1: ExtensionResultItem + HideWindowAction',
            description='Click to hide window and close extension',
            on_enter=HideWindowAction()
        ))

        # Test 2: ExtensionResultItem with CopyToClipboardAction
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 2: CopyToClipboardAction',
            description='Click to copy text to clipboard',
            on_enter=CopyToClipboardAction('Hello from Ulauncher API test!')
        ))

        # Test 3: ExtensionResultItem with DoNothingAction
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 3: DoNothingAction',
            description='Click to do nothing',
            on_enter=DoNothingAction()
        ))

        # Test 4: ExtensionResultItem with OpenUrlAction
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 4: OpenUrlAction',
            description='Click to open a URL',
            on_enter=OpenUrlAction('https://github.com/Ulauncher/Ulauncher')
        ))

        # Test 5: ExtensionResultItem with RunScriptAction
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 5: RunScriptAction',
            description='Click to run a script (echo)',
            on_enter=RunScriptAction('echo "Test script executed"')
        ))

        # Test 6: ExtensionResultItem with SetUserQueryAction
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 6: SetUserQueryAction',
            description='Click to set user query',
            on_enter=SetUserQueryAction('test new query')
        ))

        # Test 7: ExtensionResultItem with ExtensionCustomAction
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 7: ExtensionCustomAction (keep open)',
            description='Click to trigger custom action with keep_app_open=True',
            on_enter=ExtensionCustomAction(
                {'test': 'custom_data', 'action': 'test7'},
                keep_app_open=True
            )
        ))

        # Test 8: ExtensionResultItem with ExtensionCustomAction (close app)
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 8: ExtensionCustomAction (close app)',
            description='Click to trigger custom action with keep_app_open=False',
            on_enter=ExtensionCustomAction(
                {'test': 'custom_data', 'action': 'test8'},
                keep_app_open=False
            )
        ))

        # Test 9: ExtensionSmallResultItem
        items.append(ExtensionSmallResultItem(
            icon='images/icon.png',
            name='Test 9: ExtensionSmallResultItem (no description)',
            on_enter=HideWindowAction()
        ))

        # Test 10: Item with query argument
        if query:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Test 10: Query argument echo',
                description=f'You typed: "{query}"',
                on_enter=CopyToClipboardAction(query)
            ))
        else:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Test 10: Query argument echo',
                description='Type something after "test " to see it here',
                on_enter=DoNothingAction()
            ))

        # Test 11: Extension preferences
        try:
            test_option = extension.preferences.get('test_option', 'N/A')
            test_select = extension.preferences.get('test_select', 'N/A')
            test_text = extension.preferences.get('test_text', 'N/A')
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Test 11: Preferences',
                description=f'test_option={test_option}, test_select={test_select}, test_text={repr(test_text)}',
                on_enter=DoNothingAction()
            ))
        except Exception as e:
            logger.error(f"Error accessing preferences: {e}")
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Test 11: Preferences (error)',
                description=str(e),
                on_enter=DoNothingAction()
            ))

        # Test 13: OpenAction with directory
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 13: OpenAction (directory)',
            description='Click to open home directory',
            on_enter=OpenAction(os.path.expanduser('~'))
        ))

        # Test 14: ActionList (multiple actions in sequence)
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Test 14: ActionList',
            description='Click to run CopyToClipboard + SetUserQuery together',
            on_enter=ActionList([
                CopyToClipboardAction('ActionList test'),
                SetUserQueryAction('action list done')
            ])
        ))

        extension._cached_items = items
        return paginate_items(items, 0)


class ItemEnterEventListener(EventListener):
    """Handles item enter/click events"""

    def on_event(self, event, extension):
        """
        Handle item enter events from ExtensionCustomAction items
        """
        logger.info(f"ItemEnterEvent: data={event.get_data()}")

        data = event.get_data()

        if isinstance(data, dict):
            action = data.get('action', 'unknown')

            if action == 'next_page':
                page = data.get('page', 0)
                return paginate_items(extension._cached_items, page)

            if action == 'test7':
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name='Custom Action Result (Test 7)',
                        description='This appeared after clicking Test 7',
                        on_enter=HideWindowAction()
                    )
                ])

            elif action == 'test8':
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name='Custom Action Result (Test 8)',
                        description='This appeared after clicking Test 8',
                        on_enter=HideWindowAction()
                    )
                ])

        return DoNothingAction()


class PreferencesUpdateEventListener(EventListener):
    """Handles preference update events"""

    def on_event(self, event, extension):
        logger.info(f"PreferencesUpdateEvent: id={event.id}, old_value={repr(event.old_value)}, new_value={repr(event.new_value)}")


class SystemExitEventListener(EventListener):
    """Handles system exit events"""

    def on_event(self, event, extension):
        logger.info(f"SystemExitEvent: {event.__dict__}")


class PreferencesEventListener(EventListener):
    """Handles preferences load events"""

    def on_event(self, event, extension):
        logger.info(f"PreferencesEvent: preferences={event.preferences}")


if __name__ == '__main__':
    import os
    APICompatibilityTestExtension().run()
