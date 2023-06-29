# Install Nginx package
package { 'nginx':
  ensure => installed,
}

# Remove default Nginx configuration
file { '/etc/nginx/sites-enabled/default':
  ensure => absent,
}

# Define Nginx configuration file
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => "
    server {
      listen 80;
      server_name _;

      location / {
        return 301 http://\$host/redirect_me;
      }

      location /redirect_me {
        return 301 http://\$host/hello;
      }

      location /hello {
        return 200 'Hello World!';
      }
    }
  ",
  notify  => Service['nginx'],
}

# Enable the Nginx configuration
file { '/etc/nginx/sites-enabled/default':
  ensure => link,
  target => '/etc/nginx/sites-available/default',
  notify => Service['nginx'],
}

# Ensure Nginx service is running and enabled
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-enabled/default'],
}

