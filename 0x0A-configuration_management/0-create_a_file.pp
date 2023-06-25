#creates a file with permissions and groups

file {'school':
    ensure  => 'present',
    path    => '/tmp/school',
    content => 'I love Puppet',
    owner   => 'www-data',
    group   => 'www-data',
    mode    => '0744'
}
