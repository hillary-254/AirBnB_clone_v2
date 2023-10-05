# Ensure Nginx is installed
package { 'nginx':
  ensure => 'installed',
}

# Create necessary directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => 'directory',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>',
}

# Give ownership to ubuntu user and group recursively
file { '/data':
  owner => 'ubuntu',
  group => 'ubuntu',
  recurse => true,
}

# Create or recreate symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force => true,
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  content => template('path/to/your/nginx-config.erb'),
  require => Package['nginx'],
  notify => Service['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure => 'running',
  enable => true,
}
