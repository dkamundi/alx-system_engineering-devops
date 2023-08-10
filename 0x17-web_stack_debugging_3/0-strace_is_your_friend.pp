# Puppet manifest to fix file extension typo and restart Apache service

# Fix file extension typo using sed
exec { 'replace phpp with php':
  command => 'sed -i s/phpp/php/g /var/www/html/wp-settings.php',
  path    => '/usr/local/bin/:/bin/',
  require => File['/var/www/html/wp-settings.php'],  # Ensure the file exists before running the command
}

# Restart Apache service
service { 'apache2':
  ensure  => 'running',
  enable  => true,
  require => Exec['replace phpp with php'],  # Restart Apache after fixing the file
}
