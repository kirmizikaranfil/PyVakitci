[Setup]
AppId={{e4b0d240-ad26-450d-abb1-a3619274df91}
AppName=PyVakitci
AppVersion=1.6
AppVerName=PyVakitci 1.6
AppPublisherURL=http://code.google.com/p/pyvakitci
AppSupportURL=http://code.google.com/p/pyvakitci
AppUpdatesURL=http://code.google.com/p/pyvakitci
DefaultDirName={pf}\PyVakitci
DefaultGroupName=PyVakitci
AllowNoIcons=yes
LicenseFile=C:\Lisans.txt
OutputDir=C:\Users\Rahman Yazgan\Desktop
OutputBaseFilename=pyvakitci-1.6-kurulum
SetupIconFile=
Compression=lzma
SolidCompression=yes
 
[Code]
// Y�kl� olan s�r�m� kontrol edip eski s�r�m kald�r�ld�ktan sonra yeni s�r�m kurulur.
// Her s�r�mde AppId ayn� olmal�.
// http://www.lextm.com/2007/08/inno-setup-script-sample-for-version-comparison-2

// OutputDir b�l�m�n� kendinize g�re d�zenlemelisiniz.

function GetNumber(var temp: String): Integer;
var
  part: String;
  pos1: Integer;
begin
  if Length(temp) = 0 then
  begin
    Result := -1;
    Exit;
  end;
    pos1 := Pos('.', temp);
    if (pos1 = 0) then
    begin
      Result := StrToInt(temp);
    temp := '';
    end
    else
    begin
    part := Copy(temp, 1, pos1 - 1);
      temp := Copy(temp, pos1 + 1, Length(temp));
      Result := StrToInt(part);
    end;
end;
 
function CompareInner(var temp1, temp2: String): Integer;
var
  num1, num2: Integer;
begin
    num1 := GetNumber(temp1);
  num2 := GetNumber(temp2);
  if (num1 = -1) or (num2 = -1) then
  begin
    Result := 0;
    Exit;
  end;
      if (num1 > num2) then
      begin
        Result := 1;
      end
      else if (num1 < num2) then
      begin
        Result := -1;
      end
      else
      begin
        Result := CompareInner(temp1, temp2);
      end;
end;
 
function CompareVersion(str1, str2: String): Integer;
var
  temp1, temp2: String;
begin
    temp1 := str1;
    temp2 := str2;
    Result := CompareInner(temp1, temp2);
end;

const
WM_QUIT = 18;

function InitializeSetup(): Boolean;
var
  oldVersion: String;
  uninstaller: String;
  ErrorCode: Integer;
  winHwnd: longint;
  resultClose : boolean;
  retVal : boolean;
  strProg: string;
begin

  resultClose := true;
  try
    strProg := 'PyVakitci';
    winHwnd := FindWindowByWindowName(strProg);
    Log('winHwnd: ' + inttostr(winHwnd));
    if winHwnd <> 0 then
      retVal:=postmessage(winHwnd,WM_QUIT,0,0);
      if retVal then
        resultClose := True
      else
        resultClose := False;

  except
  end;

  if RegKeyExists(HKEY_LOCAL_MACHINE,
    'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{e4b0d240-ad26-450d-abb1-a3619274df91}_is1') then
  begin
    RegQueryStringValue(HKEY_LOCAL_MACHINE,
      'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{e4b0d240-ad26-450d-abb1-a3619274df91}_is1',
      'DisplayVersion', oldVersion);

    // Her yeni g�ncelleme de 1.7 olan k�sm�n de�eri att�r�lmal�d�r.
    if (CompareVersion(oldVersion, '1.703') < 0) then
    begin
      if MsgBox('PyVakitci ' + oldVersion + ' y�kl�. En g�ncel PyVakitci program�n� kurmak ister misiniz?',
        mbConfirmation, MB_YESNO) = IDNO then
      begin
        Result := False;
      end
      else
      begin
          RegQueryStringValue(HKEY_LOCAL_MACHINE,
            'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{e4b0d240-ad26-450d-abb1-a3619274df91}_is1',
            'UninstallString', uninstaller);
          ShellExec('runas', uninstaller, '/SILENT', '', SW_HIDE, ewWaitUntilTerminated, ErrorCode);
          Result := True;
      end;
    end
    else
    begin
      MsgBox('PyVakitci ' + oldVersion + ' zaten y�kl�.',
        mbInformation, MB_OK);
      Result := False;
    end;
  end
  else
  begin
    Result := True;
  end;
end;

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "C:\pyvakitci-windows-src-qt4-v1.6\build\exe.win32-3.4\PyVakitci.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\pyvakitci-windows-src-qt4-v1.6\build\exe.win32-3.4\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\PyVakitci"; Filename: "{app}\PyVakitci.exe"; WorkingDir: "{app}\"
Name: "{group}\{cm:ProgramOnTheWeb,PyVakitci}"; Filename: "http://code.google.com/p/pyvakitci"
Name: "{group}\{cm:UninstallProgram,PyVakitci}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\PyVakitci"; Filename: "{app}\PyVakitci.exe"; WorkingDir: "{app}\"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\PyVakitci"; Filename: "{app}\PyVakitci.exe"; WorkingDir: "{app}\"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\PyVakitci.exe"; Description: "{cm:LaunchProgram,PyVakitci}"; Flags: nowait postinstall skipifsilent

