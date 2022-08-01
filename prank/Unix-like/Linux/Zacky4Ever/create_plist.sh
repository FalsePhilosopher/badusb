ROOT_FOLDER=$1
echo "
<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">
<plist version=\"1.0\">
    <dict>

        <key>Label</key>
        <string>com.zac.efron</string>

        <key>ProgramArguments</key>
        <array>
            <string>$ROOT_FOLDER/.job.sh</string>
            <string>$ROOT_FOLDER</string>
        </array>

        <key>Nice</key>
        <integer>1</integer>

        <key>StartInterval</key>
        <integer>60</integer>

        <key>RunAtLoad</key>
        <true/>

        <key>StandardErrorPath</key>
        <string>$ROOT_FOLDER/.logs</string>

        <key>StandardOutPath</key>
        <string>$ROOT_FOLDER/.logs</string>

    </dict>
</plist>
"
