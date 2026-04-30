# ASP.NET Core Deployment on Ubuntu 22.04

## Prerequisites

```bash
# Install .NET SDK and Runtime
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

sudo apt update
sudo apt install -y dotnet-sdk-8.0 dotnet-runtime-8.0 aspnetcore-runtime-8.0
```

## Verify Installation

```bash
dotnet --version
dotnet --list-sdks
dotnet --list-runtimes
```

## Deploy ASP.NET Application

### Option 1: Separate Domain

If your ASP.NET app will be on a different domain (e.g., api.rotomethiopia.org):

1. **Publish your application:**

```bash
# On your development machine
dotnet publish -c Release -o ./publish

# Upload to server
scp -r ./publish/* root@178.104.213.200:/var/www/dotnetapp/
```

2. **Create systemd service:**

```bash
sudo nano /etc/systemd/system/dotnetapp.service
```

Add:
```ini
[Unit]
Description=ASP.NET Core Application
After=network.target

[Service]
WorkingDirectory=/var/www/dotnetapp
ExecStart=/usr/bin/dotnet /var/www/dotnetapp/YourApp.dll
Restart=always
RestartSec=10
KillSignal=SIGINT
SyslogIdentifier=dotnet-app
User=www-data
Environment=ASPNETCORE_ENVIRONMENT=Production
Environment=DOTNET_PRINT_TELEMETRY_MESSAGE=false
Environment=ASPNETCORE_URLS=http://localhost:5000

[Install]
WantedBy=multi-user.target
```

3. **Start the service:**

```bash
sudo systemctl daemon-reload
sudo systemctl start dotnetapp
sudo systemctl enable dotnetapp
sudo systemctl status dotnetapp
```

4. **Configure Nginx:**

```bash
sudo nano /etc/nginx/sites-available/dotnetapp
```

Add:
```nginx
server {
    listen 80;
    server_name api.rotomethiopia.org;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection keep-alive;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

5. **Enable site:**

```bash
sudo ln -s /etc/nginx/sites-available/dotnetapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Same Domain, Different Path

If you want Django on root and ASP.NET on /api:

1. **Configure ASP.NET to use path base:**

In your `Program.cs` or `Startup.cs`:

```csharp
app.UsePathBase("/api");
app.UseRouting();
```

2. **Update Nginx configuration:**

Use the combined configuration from `nginx_multi_app.conf`

### Option 3: Different Port (Direct Access)

If you want to access ASP.NET directly on a different port:

1. **Configure ASP.NET to listen on port 5000:**

```bash
# In systemd service file
Environment=ASPNETCORE_URLS=http://0.0.0.0:5000
```

2. **Open firewall:**

```bash
sudo ufw allow 5000/tcp
```

3. **Access directly:**
- Django: http://178.104.213.200
- ASP.NET: http://178.104.213.200:5000

## Configuration Files

### appsettings.Production.json

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "ConnectionStrings": {
    "DefaultConnection": "Your connection string here"
  }
}
```

### Kestrel Configuration (if needed)

In `appsettings.json`:

```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5000"
      }
    },
    "Limits": {
      "MaxRequestBodySize": 52428800
    }
  }
}
```

## Multiple ASP.NET Apps

If you have multiple ASP.NET applications:

```bash
# App 1 on port 5000
Environment=ASPNETCORE_URLS=http://localhost:5000

# App 2 on port 5001
Environment=ASPNETCORE_URLS=http://localhost:5001

# App 3 on port 5002
Environment=ASPNETCORE_URLS=http://localhost:5002
```

Then configure Nginx to proxy to different ports based on domain or path.

## Monitoring and Logs

```bash
# View ASP.NET logs
sudo journalctl -u dotnetapp -f

# View Nginx logs
sudo tail -f /var/log/nginx/dotnet_error.log

# Restart ASP.NET app
sudo systemctl restart dotnetapp

# Check status
sudo systemctl status dotnetapp
```

## SSL Configuration

After setting up both apps:

```bash
# Get SSL for both domains
sudo certbot --nginx -d rotomethiopia.org -d www.rotomethiopia.org
sudo certbot --nginx -d api.rotomethiopia.org
```

## Performance Tips

1. **Enable response compression in ASP.NET:**

```csharp
builder.Services.AddResponseCompression();
app.UseResponseCompression();
```

2. **Configure Nginx caching for static files**

3. **Use a reverse proxy cache if needed**

4. **Monitor resource usage:**

```bash
htop
systemctl status dotnetapp
systemctl status gunicorn
```

## Troubleshooting

### ASP.NET app won't start:

```bash
# Check logs
sudo journalctl -u dotnetapp -n 50

# Test manually
cd /var/www/dotnetapp
dotnet YourApp.dll
```

### Port conflicts:

```bash
# Check what's using port 5000
sudo lsof -i :5000
sudo netstat -tulpn | grep 5000
```

### Permission issues:

```bash
sudo chown -R www-data:www-data /var/www/dotnetapp
sudo chmod -R 755 /var/www/dotnetapp
```

## Summary

You now have:
- Django (ROTOM) running on Gunicorn
- ASP.NET Core running on Kestrel
- Nginx as reverse proxy for both
- Both apps can coexist on the same server

Choose the configuration that best fits your needs!
