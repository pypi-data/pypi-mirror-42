Reset

Reset() {
	Hotkey '~LButton', 'Off'
	Hotkey 'Esc', 'Off'
	DLLCall 'SystemParametersInfo', Int, 87
}

Command(Delay, Cmds*) {
	For _, Cmd In Cmds {
		SendEvent '{Raw}' Cmd '`n'
		Sleep Delay
	}
}

Sites(Delay, URLs*) {
	For _, URL In URLs {
		Run 'http://' URL
		Sleep Delay
	}
}

Login(URL, _Fields*) {
	Global Fields := _Fields
	Run 'https://' URL
	DLLCall 'SetSystemCursor', Int, DLLCall('LoadCursor', Int, 0, Int, 32649), Int, 32513
	Hotkey '~LButton', 'On'
	Hotkey 'Esc', 'On'
}

~LButton::
	Send Fields.RemoveAt(1)
	If Fields.Count() = 0
		Reset
	Return

Esc::Reset