# Lab Center AD and Logs Management

### Environment Setip

```bash
# Create .venv
python -m venv .venv

# Activate in windows
.venv\Scripts\activate

# Activate in Linux
source .venv/Scripts/activate
```

### Running the project

```bash
python main.py
```

### Running Cron Job Reader (Custom logs)

```bash
# Run daily
python crons/runner.py

# Run fixed date
python crons/runner.py --date 2026-06-26

# Run for a date range
python crons/runner.py --start 2026-06-20 --end 2026-06-26
```

### Cron Job

```bash
# Test the command manually first
cd /var/www/labcenter && python crons/runner.py

# Edit crontab
crontab -e

# Add this line to run daily at 12:00 PM
0 12 * * * cd /var/www/labcenter && python crons/runner.py >> /var/www/labcenter/logs/analyzer.log 2>&1

# Check if cron ran successfully
tail -f /var/www/labcenter/logs/analyzer.log

# List cron jobs to confirm it's added
crontab -l
```
