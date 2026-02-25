# Check app logs
sudo journalctl -u inventory_app -f

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log

# Test Redis connection
sudo apt-get update
sudo apt-get install redis-server
redis-cli -h 10.20.10.13 -a Password123* ping
  
# Test DB connection
sudo apt update
sudo apt install postgresql-client -y
psql -h 10.20.10.2 -p 5432 -U admin -d postgres



# run the app 

source venv/bin/activate
python app.py 

