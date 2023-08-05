Shopify command-line client
###########################


Installing
==========

Install from pip::

    pip install --user shopicli


Autocompletion support
======================

For Bash::

    eval "$(_SHOPICLI_COMPLETE=source shopicli)"

For Zsh::

    eval "$(_SHOPICLI_COMPLETE=source_zsh shopicli)"



Usage
=====

The first step is to create a new connection.

Connection credentials (private app API keys) will be stored in
``~/.config/shopify``.

::

    % shopicli connection create
    Name this connection [default]: myconnection
    Store name: mystore
    Head to https://mystore.myshopify.com/admin/apps/private if you need to create a new API key.
    API key: 8e32ca37adbec46059b1f4762f5d9810
    API key password:


Most commands will require a connection name, example::

    shopicli -m myconnection products list
