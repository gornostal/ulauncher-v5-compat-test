# Ulauncher API v5 Compatibility Test Extension

This is a test extension for the Ulauncher v5 Extension API. It renders multiple result items, each testing different aspects of the API to verify compatibility and functionality.

## Project Structure

```
.
├── images/
│   └── icon.png           # Extension icon
├── manifest.json          # Extension metadata
├── versions.json          # API version mapping
├── main.py                # Main extension code
└── README.md              # This file
```

## Installation

Copy this directory to your Ulauncher extensions folder:

```bash
cp -r ulauncher-v5-compat-test ~/.local/share/ulauncher/extensions/
```

Then restart Ulauncher or reload the extension.

## Testing

Run Ulauncher in development mode:

```bash
ulauncher --no-extensions --dev -v
```

Then type `test` (or your configured keyword) to see the compatibility test items.

## API Features Tested

### 1. **Result Items**
- `ExtensionResultItem` - Full item with icon, name, description, and action
- `ExtensionSmallResultItem` - Compact item without description

### 2. **Actions**
The extension tests the following action types:

- **HideWindowAction** (Test 1) - Hides Ulauncher window
- **CopyToClipboardAction** (Test 2) - Copies text to clipboard
- **DoNothingAction** (Test 3) - Does nothing on click
- **OpenUrlAction** (Test 4) - Opens a URL in the default browser
- **RunScriptAction** (Test 5) - Executes a shell script
- **SetUserQueryAction** (Test 6) - Updates the search query
- **ExtensionCustomAction** (Tests 7-8) - Custom action with callback
  - With `keep_app_open=True` (Test 7)
  - With `keep_app_open=False` (Test 8)
- **LaunchAppAction** (Test 12) - Launches a system application
- **OpenAction** (Test 13) - Opens a file or directory

### 3. **Events**
- **KeywordQueryEvent** - Triggered when user types the keyword
- **ItemEnterEvent** - Triggered when user clicks an item with ExtensionCustomAction

### 4. **Preferences**
Tests different preference types:
- Keyword preference (`test_keyword`)
- Input preference (`test_option`)
- Select preference (`test_select`)
- Text preference (`test_text`) - renders as a textarea for multiline input

### 5. **Query Arguments**
Tests passing and handling query arguments (Test 10)

## Test Items

| # | Test | Feature |
|---|------|---------|
| 1 | ExtensionResultItem + HideWindowAction | Basic item and hide action |
| 2 | CopyToClipboardAction | Clipboard interaction |
| 3 | DoNothingAction | No-op action |
| 4 | OpenUrlAction | URL opening |
| 5 | RunScriptAction | Script execution |
| 6 | SetUserQueryAction | Query modification |
| 7 | ExtensionCustomAction (keep open) | Custom action with app staying open |
| 8 | ExtensionCustomAction (close app) | Custom action with app closing |
| 9 | ExtensionSmallResultItem | Compact item rendering |
| 10 | Query argument echo | Argument handling |
| 11 | Preferences | Reading extension preferences |
| 12 | LaunchAppAction | Application launching |
| 13 | OpenAction | File/directory opening |

## Logging

The extension logs events using Python's logging module. To see logs, run Ulauncher in verbose mode:

```bash
ulauncher -v
```

Look for log messages starting with the module name in the output.

## Debugging Tips

1. **Check logs**: Run `ulauncher -v` to see detailed logging output
2. **Reload extension**: Press `Ctrl+C` and restart Ulauncher during development
3. **Use extension preferences**: Access preferences in the Ulauncher settings UI to test preference handling

## API Version

- **Required API Version**: 2
- **Ulauncher Version**: v5+

## Notes

- Test 12 (LaunchAppAction) launches `gedit`. If gedit is not available, the action may fail silently.
- Test 13 (OpenAction) opens the home directory. Works on Linux with file managers.
- Some actions like OpenUrlAction, LaunchAppAction, and OpenAction are system-dependent and may behave differently on different distributions.
