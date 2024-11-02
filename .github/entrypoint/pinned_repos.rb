#!/usr/bin/env ruby

# get a user's pinned repos
# https://stackoverflow.com/q/43352056/4058484
# https://stackoverflow.com/q/7785793/4058484

require 'uri'
require 'rubygems'
require 'nokogiri'
require 'open-uri'

# if ARGV.length != 1
#  STDERR.puts "usage: /maps/pinned_repos.rb <username>"
#  exit 1
# end

token = ENV['INPUT_TOKEN']
username = ARGV[0]
mode = ARGV[1]

# open("http://...", :http_basic_authentication=>[user, password])
# profile_url = "https://github.com/#{username}"

profile_url = "https://github.com/#{username}?view_as=#{mode}"

uri = URI.parse( profile_url )
params = { :view_as => "#{mode}" }
uri.query = URI.encode_www_form( params )

page = Nokogiri::HTML(URI.open(profile_url, "Authorization" => "Bearer #{token}"))
page.css("span.repo").each { |repo| puts repo.text }
