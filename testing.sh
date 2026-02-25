# Check app logs
sudo journalctl -u inventory_app -f

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log

# Test Redis connection
redis-cli -h 10.20.10.13 -a Password123* ping
  
# Test DB connection
psql -h 10.20.10.2:5432 -U admin -d postgres