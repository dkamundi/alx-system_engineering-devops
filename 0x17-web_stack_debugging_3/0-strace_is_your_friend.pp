# Fix file extension typo using sed
exec { 'replace phpp with php':
  command => 'sed -i s/phpp/php/g /var/www/html/wp-settings.php',
  path    => '/usr/local/bin/:/bin/'
}

# Restart Apache service
exec { 'restart apache2 service':
  command => 'service apache2 restart',
  provider => shell
}

