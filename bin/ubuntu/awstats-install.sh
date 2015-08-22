sudo apt-get install awstats munin php5-fpm libgeo-ipfree-perl libnet-ip-perl libgeo-ip-perl

sudo perl -p -i'.bak' -e 's/www-data/webapps/g' /etc/nginx/nginx.conf
sudo perl -p -i'.bak' -e 's/www-data/webapps/g' /etc/php5/fpm/pool.d/www.conf

#rsync -aP etc/awstats/awstats.conf europe:/etc/nginx/sites-enabled/awstats.conf
sudo cp etc/awstats/awstats.conf /etc/nginx/sites-enabled/
sudo cp etc/awstats/cgi-bin.php /etc/nginx/

sudo mkdir -p /var/www/awstats
sudo chown -R webapps:webapps /var/www/awstats
# sudo chmod -R 755 /var/www/awstats

sudo mkdir /var/lib/awstats//
sudo chown -R webapps:webapps /var/lib/awstats/
# sudo chmod -R 755 /var/lib/awstats/

sudo chown -R webapps:webapps /var/log/nginx

# sudo /usr/share/awstats/tools/awstats_buildstaticpages.pl -config= -dir=/var/www/awstats/ -staticlinks -awstatsprog=/usr/lib/cgi-bin/awstats.pl

wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz

unzip GeoIP.dat.gz
unzip GeoLiteCity.dat.gz

sudo mv GeoIP.dat /usr/local/lib/
sudo mv GeoLiteCity.dat /usr/local/lib/GeoIPCity.dat

sudo chown webapps:webapps /usr/local/lib/GeoIP.dat
sudo chown webapps:webapps /usr/local/lib/GeoLiteCity.dat

sudo apt-get install munin spawn-fcgi

sudo spawn-fcgi -s /var/run/munin/fastcgi-graph.sock -U webapps -u munin -g munin /usr/lib/munin/cgi/munin-cgi-graph
sudo spawn-fcgi -s /var/run/munin/fastcgi-html.sock  -U webapps -u munin -g munin /usr/lib/munin/cgi/munin-cgi-html
