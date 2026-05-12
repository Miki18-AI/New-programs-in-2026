#Requires AutoHotkey v2.0

; Состояние кликера
Toggled := false

F1:: {
    global Toggled := !Toggled
    
    if Toggled {
        ; Устанавливаем интервал ~83 мс для 12 кликов в секунду
        SetTimer(DoClick, 60)
        ToolTip("Кликер (12 CPS): ВКЛ")
    } else {
        SetTimer(DoClick, 0)
        ToolTip("Кликер: ВЫКЛ")
    }
    
    SetTimer(() => ToolTip(), -1000)
}

DoClick() {
    Click()
}

; Выход из скрипта
F2::ExitApp