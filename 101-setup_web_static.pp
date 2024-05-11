# This puppet manifest configures nginx webserver

exec { 'apt update':
    command => '/usr/bin/apt update'
}

package { 'nginx':
    ensure  => 'installed',
    require => Exec['apt update']
}

file { '/data/':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755'
}

file { '/data/web_static/':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755'
}

file { '/data/web_static/releases/':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755'
}

file { '/data/web_static/releases/test/':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755'
}

file { '/data/web_static/releases/test/index.html':
    ensure  => 'present',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0644',
    content => @(CONTENT)
<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
</html>
    CONTENT
}

file { '/data/web_static/current':
    ensure => 'link',
    target => '/data/web_static/releases/test/'
}

file { '/etc/nginx/sites-available/default':
    ensure  => 'present',
    owner   => 'root',
    group   => 'root',
    content => @(CONTENT)
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location /hbnb_static/ {
                alias /data/web_static/current/;
        }
        error_page 404 /custom_404.html;
        location = /custom_404.html {
                root /usr/share/nginx/html;
                internal;
        }
        rewrite ^/redirect_me$ https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
                add_header X-Served-By $HOSTNAME;
        }
}
    CONTENT
}

file { '/etc/nginx/sites-enabled/default':
    ensure => 'link',
    target => '/etc/nginx/sites-available/default',
    owner  => 'ubuntu',
    group  => 'ubuntu'
}

service { 'nginx':
    ensure     => 'running',
    enable     => true,
    hasrestart => true
}
