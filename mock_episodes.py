mock_episodes = [
    {
        "goal": "Uninstall the Slack app",
        "observations": [
            {"app": "Settings", "ui_elements": ["Apps", "Battery", "Search"]},
            {"app": "Apps", "ui_elements": ["Slack", "Gmail", "Maps"]},
            {"app": "Slack", "ui_elements": ["Force Stop", "Uninstall", "Storage"]}
        ],
        "ground_truth_actions": [
            'CLICK("Apps")',
            'CLICK("Slack")',
            'CLICK("Uninstall")'
        ]
    },
    {
        "goal": "Send an SMS to Alice saying 'See you soon'",
        "observations": [
            {"app": "Home", "ui_elements": ["Messages", "Contacts", "Browser"]},
            {"app": "Messages", "ui_elements": ["New Message", "Search"]},
            {"app": "New Message", "ui_elements": ["To", "Message body", "Send"]}
        ],
        "ground_truth_actions": [
            'CLICK("Messages")',
            'CLICK("New Message")',
            'CLICK("To")',
            'TYPE("Alice")',
            'CLICK("Message body")',
            'TYPE("See you soon")',
            'CLICK("Send")'
        ]
    },
    {
        "goal": "Open the Stopwatch tab in the Clock app",
        "observations": [
            {"app": "Clock", "ui_elements": ["Alarm", "Stopwatch", "Timer"]},
        ],
        "ground_truth_actions": [
            'CLICK("Stopwatch")'
        ]
    },
    {
        "goal": "Add a new contact named 'John Doe'",
        "observations": [
            {"app": "Contacts", "ui_elements": ["Add Contact", "Search", "Settings"]},
            {"app": "Add Contact", "ui_elements": ["Name", "Phone", "Save"]}
        ],
        "ground_truth_actions": [
            'CLICK("Add Contact")',
            'CLICK("Name")',
            'TYPE("John Doe")',
            'CLICK("Save")'
        ]
    },
    {
        "goal": "Turn on Airplane Mode",
        "observations": [
            {"app": "Settings", "ui_elements": ["Network", "Display", "Battery"]},
            {"app": "Network", "ui_elements": ["Wi-Fi", "Mobile Data", "Airplane Mode"]}
        ],
        "ground_truth_actions": [
            'CLICK("Network")',
            'CLICK("Airplane Mode")'
        ]
    },
    {
        "goal": "Search for 'weather' using the browser",
        "observations": [
            {"app": "Home", "ui_elements": ["Browser", "Camera", "Settings"]},
            {"app": "Browser", "ui_elements": ["Search bar", "Bookmarks"]},
        ],
        "ground_truth_actions": [
            'CLICK("Browser")',
            'CLICK("Search bar")',
            'TYPE("weather")',
            'PRESS("Enter")'
        ]
    },
    {
        "goal": "Mute all notification sounds",
        "observations": [
            {"app": "Settings", "ui_elements": ["Sound", "Display", "Battery"]},
            {"app": "Sound", "ui_elements": ["Volume", "Do Not Disturb", "Vibration"]},
        ],
        "ground_truth_actions": [
            'CLICK("Sound")',
            'CLICK("Do Not Disturb")'
        ]
    },
    {
        "goal": "Set a timer for 10 minutes",
        "observations": [
            {"app": "Clock", "ui_elements": ["Alarm", "Stopwatch", "Timer"]},
            {"app": "Timer", "ui_elements": ["Set time", "Start", "Cancel"]}
        ],
        "ground_truth_actions": [
            'CLICK("Timer")',
            'CLICK("Set time")',
            'TYPE("10:00")',
            'CLICK("Start")'
        ]
    },
    {
        "goal": "Enable dark mode",
        "observations": [
            {"app": "Settings", "ui_elements": ["Display", "Battery", "Network"]},
            {"app": "Display", "ui_elements": ["Brightness", "Dark Mode", "Font Size"]}
        ],
        "ground_truth_actions": [
            'CLICK("Display")',
            'CLICK("Dark Mode")'
        ]
    },
    {
        "goal": "Open Gmail app from the home screen",
        "observations": [
            {"app": "Home", "ui_elements": ["Gmail", "Calendar", "Photos"]}
        ],
        "ground_truth_actions": [
            'CLICK("Gmail")'
        ]
    }
]
