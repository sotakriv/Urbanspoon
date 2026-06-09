# Urbanspoon Local Server - Reverse Engineering Project

## What is this?
This is a local Flask server that mimics the Urbanspoon API, allowing old versions of the Urbanspoon iOS app (circa 2010, v=14) to connect to a custom backend instead of the now-defunct Urbanspoon servers (acquired by Zomato in 2015).

## Setup

### Requirements
- Python 3.x
- Flask (`pip install flask`)
- A jailbroken iPhone running iOS 6 (tested on iPhone 5, iOS 6.1.3)
- The Urbanspoon IPA (version 1.15, app version 14)

### Steps

**1. Install Flask**
```
pip install flask
```

**2. Run the server**
```
python server.py
```
Server runs on port 80. Note: on Windows you may need to run CMD as Administrator.

**3. Find your PC's local IP**
```
ipconfig
```
Look for IPv4 Address (e.g. 192.168.1.X)

**4. On the jailbroken iPhone, edit /private/etc/hosts**
Add these lines (replace X with your PC's IP):
```
192.168.X.X  www.urbanspoon.com
192.168.X.X  www.zomato.com
192.168.X.X  data.flurry.com
192.168.X.X  api.apptentive.com
```

**5. Install the Urbanspoon IPA**
Use iFile or similar to install the IPA on the jailbroken device.

---

## Known Issues / Help Needed

### Main Problem: App crashes after shake (ispin)
The app successfully:
- Connects to our server
- Calls `/api/ihello` and receives plist response
- Calls `/api/ispin` after shaking
- Receives plist response

But then crashes with `EXC_CRASH (SIGABRT)` immediately after receiving the ispin response.

**Crash log excerpt:**
```
Exception Type:  EXC_CRASH (SIGABRT)
Last Exception Backtrace:
(0x312823e2 0x38f7d95e 0x311cd218 0x82f8 0x9332 0x84a6)

Thread 0 Crashed:
14  urbanspin  0x000029d2  0x1000 + 6610
15  urbanspin  0x00002970  0x1000 + 6512
```

**What we've tried:**
- Returning JSON, XML, plist formats from ispin
- Empty responses
- Various plist key combinations (obj_id, title, address, cuisine_id, neighborhood_id, price_id, distance_miles, etc.)
- Redirect to mobile restaurant page
- Clearing app cache and NSUserDefaults

**What we know:**
- The binary is FairPlay DRM encrypted (cryptid=1), so we can't read/patch the code directly
- The crash happens at the same code address regardless of server response
- The app uses a UIPickerView with 3 reels (cuisine, neighborhood, price) fed by ihello
- The SpinScreen has `updateReel:animated:` method which is likely where it crashes
- Strings in the binary appear obfuscated

**What we need help with:**
1. Decrypting the binary (Clutch2 not working on this device)
2. Understanding what exact plist keys `ispin` should return
3. Whether the crash is in the picker animation or data parsing
4. Any experience with this specific Urbanspoon version (v=14, 2010)

---

## API Endpoints Discovered

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ihello` | GET | Initial handshake, returns city/cuisines/neighborhoods/prices |
| `/api/ispin` | GET | Called on shake, should return restaurant data |
| `/api/lists` | GET | Restaurant lists |
| `/api/icheck_auth` | GET | Auth check |
| `/api/ad_zones` | GET | Ad zones (return empty) |
| `/api/ad_spin` | GET | Spin ads (return empty) |
| `/aap.do` | POST | Flurry analytics (return ok) |
| `/aas.do` | POST | Flurry analytics (return ok) |

---

## Current ihello response format (plist)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist ...>
<plist version="1.0">
<dict>
    <key>status</key><string>ok</string>
    <key>version</key><integer>14</integer>
    <key>city</key><string>New York</string>
    <key>country</key><string>US</string>
    <key>within</key><integer>1000</integer>
    <key>lat</key><real>40.7128</real>
    <key>lon</key><real>-74.0060</real>
    <key>neighborhoods</key><array>
        <dict><key>obj_id</key><integer>0</integer><key>title</key><string>Any Area</string></dict>
        <dict><key>obj_id</key><integer>1</integer><key>title</key><string>Manhattan</string></dict>
    </array>
    <key>cuisines</key><array>
        <dict><key>obj_id</key><integer>0</integer><key>title</key><string>Any Food</string></dict>
        <dict><key>obj_id</key><integer>1</integer><key>title</key><string>American</string></dict>
    </array>
    <key>prices</key><array>
        <dict><key>obj_id</key><integer>0</integer><key>title</key><string>Any Price</string></dict>
        <dict><key>obj_id</key><integer>1</integer><key>title</key><string>$</string></dict>
    </array>
</dict>
</plist>
```
