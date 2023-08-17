# nginx_traffic_increase.pp

# Adjust worker_processes in nginx.conf
file { '/etc/nginx/nginx.conf':
  ensure  => present,
  content => file('/etc/nginx/nginx.conf')
              .content
              .gsub('worker_processes 15;', 'worker_processes 4;'),
  notify  => Service['nginx'],
}

# Define Nginx service
service { 'nginx':
  ensure     => running,
  enable     => true,
  hasrestart => true,
  hasstatus  => true,
  require    => File['/etc/nginx/nginx.conf'],
}

