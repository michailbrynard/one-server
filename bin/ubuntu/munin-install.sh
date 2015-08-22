#munin

sudo apt-get install munin munin-node

sudo htpasswd -c /etc/nginx/htpasswd admin
sudo chown webapps:webapps /et/nginx/htpasswd

# Ensure this is in nginx config
   location /munin/static/ {
        alias /etc/munin/static/;
        expires modified +1w;
    }

    location /munin/ {
        auth_basic            "Restricted";
        # Create the htpasswd file with the htpasswd tool.
        auth_basic_user_file  /etc/nginx/htpasswd;

        alias /var/cache/munin/www/;
        expires modified +310s;
    }

