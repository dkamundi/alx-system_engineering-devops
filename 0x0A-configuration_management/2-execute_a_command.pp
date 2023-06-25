# Executes a bash command
exec { 'killmenow_process':
  command => 'pkill -f killmenow',
  path    => '/usr/bin:/usr/sbin:/bin',
  onlyif  => 'pgrep -f killmenow',
}
