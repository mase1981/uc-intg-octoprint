# OctoPrint Integration for Unfolded Circle Remote 2/3

Control your OctoPrint 3D printer directly from your Unfolded Circle Remote 2 or Remote 3 with comprehensive print control, **full remote UI layout**, **real-time state monitoring**, and **complete REST API-based control**.

![OctoPrint](https://img.shields.io/badge/OctoPrint-3D%20Printer-green)
[![GitHub Release](https://img.shields.io/github/v/release/mase1981/uc-intg-octoprint?style=flat-square)](https://github.com/mase1981/uc-intg-octoprint/releases)
![License](https://img.shields.io/badge/license-MPL--2.0-blue?style=flat-square)
[![GitHub issues](https://img.shields.io/github/issues/mase1981/uc-intg-octoprint?style=flat-square)](https://github.com/mase1981/uc-intg-octoprint/issues)
[![Community Forum](https://img.shields.io/badge/community-forum-blue?style=flat-square)](https://community.unfoldedcircle.com/)
[![Discord](https://badgen.net/discord/online-members/zGVYf58)](https://discord.gg/zGVYf58)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/mase1981/uc-intg-octoprint/total?style=flat-square)
[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat-square)](https://buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-donate-blue.svg?style=flat-square)](https://paypal.me/mmiyara)
[![Github Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-30363D?&logo=GitHub-Sponsors&logoColor=EA4AAA&style=flat-square)](https://github.com/sponsors/mase1981)


## Features

This integration provides comprehensive control of OctoPrint 3D printers through the native REST API, delivering seamless integration with your Unfolded Circle Remote for complete 3D printing control.

---
## ❤️ Support Development ❤️

If you find this integration useful, consider supporting development:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/mase1981)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/mmiyara)

Your support helps maintain this integration. Thank you! ❤️
---

### 🖨️ **Print Job Control**

#### **Button Entities**
- **Pause Job** - Pause active print job
- **Resume Job** - Resume paused print job
- **Stop Job** - Cancel/stop current print job
- **Home Printer** - Home all axes (X, Y, Z)
- **Connect Printer** - Connect OctoPrint to printer
- **Disconnect Printer** - Disconnect OctoPrint from printer

### 🎮 **Remote Entity**

#### **Full UI Layout**
Pre-configured button layout optimized for Remote UI:
- **Print Controls** - Pause, Resume, Stop buttons
- **Connection Controls** - Connect, Disconnect buttons
- **Home Controls** - Home all axes button
- **Jog Controls** - X/Y/Z axis jogging (separate page)
  - X+/X- buttons (10mm steps)
  - Y+/Y- buttons (10mm steps)
  - Z+/Z- buttons (1mm steps)
- **Individual Axis Homing** - Home X, Y, Z separately

#### **Activity Integration**
- Works seamlessly with Remote activities
- Simple command support for custom macros
- Pre-configured button mappings

### 📊 **Sensor Entities**

Real-time monitoring of printer state:

- **Status Sensor** - Current printer state (Operational, Printing, Paused, etc.)
- **Progress Sensor** - Print completion percentage
- **Time Remaining Sensor** - Estimated time remaining for print
- **File Sensor** - Currently loaded file name
- **Connection Sensor** - Integration connection status

### **Protocol Requirements**

- **Protocol**: OctoPrint REST API
- **Port**: 80 (HTTP) or 443 (HTTPS)
- **API Key**: Required (obtainable from OctoPrint Settings → API)
- **Network Access**: OctoPrint server must be on same local network
- **Connection**: Periodic polling for state updates
- **Real-time Updates**: Status updated every 5 seconds

### **Network Requirements**

- **Local Network Access** - Integration requires same network as OctoPrint server
- **HTTP/HTTPS Protocol** - REST API over HTTP (port 80) or HTTPS (port 443)
- **Static IP Recommended** - OctoPrint server should have static IP or DHCP reservation
- **Firewall** - Must allow HTTP/HTTPS traffic
- **API Key** - Required authentication via X-Api-Key header

## Installation

### Option 1: Remote Web Interface (Recommended)
1. Navigate to the [**Releases**](https://github.com/mase1981/uc-intg-octoprint/releases) page
2. Download the latest `uc-intg-octoprint-<version>-aarch64.tar.gz` file
3. Open your remote's web interface (`http://your-remote-ip`)
4. Go to **Settings** → **Integrations** → **Add Integration**
5. Click **Upload** and select the downloaded `.tar.gz` file

### Option 2: Docker (Advanced Users)

The integration is available as a pre-built Docker image from GitHub Container Registry:

**Image**: `ghcr.io/mase1981/uc-intg-octoprint:latest`

**Docker Compose:**
```yaml
services:
  uc-intg-octoprint:
    image: ghcr.io/mase1981/uc-intg-octoprint:latest
    container_name: uc-intg-octoprint
    network_mode: host
    volumes:
      - </local/path>:/data
    environment:
      - UC_CONFIG_HOME=/data
      - UC_INTEGRATION_HTTP_PORT=9090
      - UC_INTEGRATION_INTERFACE=0.0.0.0
      - PYTHONPATH=/app
    restart: unless-stopped
```

**Docker Run:**
```bash
docker run -d --name uc-octoprint --restart unless-stopped --network host -v octoprint-config:/app/config -e UC_CONFIG_HOME=/app/config -e UC_INTEGRATION_INTERFACE=0.0.0.0 -e UC_INTEGRATION_HTTP_PORT=9090 -e PYTHONPATH=/app ghcr.io/mase1981/uc-intg-octoprint:latest
```

## Configuration

### Step 1: Prepare Your OctoPrint Server

**IMPORTANT**: OctoPrint must be running and accessible on your network before adding the integration.

#### Obtain API Key:
1. Open OctoPrint web interface
2. Go to **Settings** (wrench icon)
3. Navigate to **API** section
4. Copy the **API Key** (or generate a new one)

#### Verify Network Connection:
1. Check that OctoPrint server is accessible on your network
2. Note the IP address or hostname
3. Note the port (usually 80 for HTTP or 443 for HTTPS)
4. Ensure API is enabled (enabled by default)

#### Network Setup:
- **Connection**: Ethernet or Wi-Fi
- **Static IP**: Recommended via DHCP reservation
- **Firewall**: Allow HTTP/HTTPS traffic
- **Network Isolation**: Must be on same subnet as Remote

### Step 2: Setup Integration

1. After installation, go to **Settings** → **Integrations**
2. The OctoPrint integration should appear in **Available Integrations**
3. Click **"Configure"** to begin setup:

#### **Configuration:**
- **Device Name**: Friendly name (e.g., "My 3D Printer")
- **IP Address or Hostname**: Enter OctoPrint server IP (e.g., 192.168.1.100)
- **Port**: Default is 80 (or 443 for HTTPS)
- **API Key**: Paste the API key from OctoPrint
- **Use SSL**: Check if using HTTPS
- **Path**: Default is "/" (change if OctoPrint is at a subpath like "/octoprint/")
- Click **Complete Setup**

#### **Connection Test:**
- Integration verifies server connectivity
- REST API connection established
- Setup fails if server unreachable or API key invalid

4. Integration will create entities:
   - **Buttons**: Pause, Resume, Stop, Home, Connect, Disconnect
   - **Remote**: `remote.octoprint_[device_name]`
   - **Sensors**: Multiple sensor entities for state monitoring

## Using the Integration

### Button Entities

Individual button entities for each control:

- **Pause Job**: Pause the currently printing job
- **Resume Job**: Resume a paused job
- **Stop Job**: Cancel and stop the current job
- **Home Printer**: Home all printer axes
- **Connect Printer**: Connect OctoPrint to the printer
- **Disconnect Printer**: Disconnect OctoPrint from the printer

### Remote Entity

The remote entity provides:
- **Print Control Page**: Pause, Resume, Stop, Home, Connect, Disconnect
- **Jog Control Page**: Axis jogging and individual axis homing
- **Activity Support**: All buttons work in activities

### Sensor Entities

| Sensor | Description |
|--------|-------------|
| Status Sensor | Current printer operational state |
| Progress Sensor | Print completion percentage (0-100%) |
| Time Remaining Sensor | Estimated time left in format HH:MM:SS |
| File Sensor | Name of currently loaded G-code file |
| Connection Sensor | Integration connection status |

## Credits

- **Developer**: Meir Miyara
- **OctoPrint**: Open-source 3D printer web interface
- **Unfolded Circle**: Remote 2/3 integration framework (ucapi)
- **Protocol**: OctoPrint REST API
- **Community**: Testing and feedback from UC community

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0) - see LICENSE file for details.

## Support & Community

- **GitHub Issues**: [Report bugs and request features](https://github.com/mase1981/uc-intg-octoprint/issues)
- **UC Community Forum**: [General discussion and support](https://unfolded.community/)
- **Developer**: [Meir Miyara](https://www.linkedin.com/in/meirmiyara)
- **OctoPrint Support**: [Official OctoPrint Documentation](https://docs.octoprint.org/)

---

**Made with ❤️ for the Unfolded Circle and OctoPrint Communities**

**Thank You**: Meir Miyara
