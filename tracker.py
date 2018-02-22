import sys
import os
import string
import random
import hashlib
import urllib.parse
from bs4 import BeautifulSoup

def generate_css(path, duration=100, keyframe_count=100):
	inject_template_tag(path)

	with open(path, 'r') as f:
		soup = BeautifulSoup(f.read(), 'html.parser')

	selectors = []
	generate_tag_selectors(soup, selectors, '')

	if not os.path.exists('./static/css/'):
	    os.makedirs('./static/css/')

	with open('static/css/tracker.css', 'w') as f:
		for selector in selectors:
			animation_name = ''.join(random.choices(string.ascii_lowercase, k=6))
			f.write(generate_animation_keyframes(selector, animation_name, duration, keyframe_count))
			f.write(generate_animation_rule(selector, animation_name, duration))
			f.write(generate_hover_rule(selector))

def generate_hover_rule(selector):
	return '{selector}:hover {{ -webkit-animation-play-state:running; -moz-animation-play-state:running; animation-play-state:running; }}\n'.format(selector=selector)

def generate_animation_rule(selector, animation_name, duration):
	return '{selector} {{ -moz-animation: {animation_name} {duration}s infinite; -webkit-animation: {animation_name} {duration}s infinite; animation: {animation_name} {duration}s infinite; -webkit-animation-play-state:paused; -moz-animation-play-state:paused; animation-play-state:paused; }}\n'.format(selector=selector, animation_name=animation_name, duration=duration)

def generate_animation_keyframes(selector, animation_name, duration, keyframe_count):
	keyframe_count = max(1, min(10000, keyframe_count))
	step_size = 100.00 / keyframe_count
	time_per_step = float(duration) / keyframe_count

	keyframes = []
	i = 0
	time = 0
	while i < 100:
		percentage, t = '{0:.2f}'.format(i), '{0:.2f}'.format(time)
		keyframes.append('%s%% { background-image: url("http://127.0.0.1:5000/tracker/%s/%s/"); }' % (percentage, urllib.parse.quote(selector), t))
		i += step_size
		time += time_per_step

	return '@keyframes %s { %s }\n' % (animation_name, ' '.join(keyframes))

def inject_template_tag(path):
	with open(path, 'r') as f:
		html = f.read()

	if html.find('<head>{css_tracker_import_line}') > -1:
		return

	html = html.replace('<head>', '<head>{css_tracker_import_line}')

	with open(path, 'w') as f:
		f.write(html)	

def generate_tag_selectors(s, selectors, selector):
	if getattr(s, 'name', None) == None:
		return

	if selector:
		selectors.append(selector)

	if hasattr(s, 'children'):
		i = 1
		for child in s.children:
			if getattr(child, 'name', None) == None:
				continue
			next_selector = selector + ' :nth-child(%s)' % (i)
			generate_tag_selectors(child, selectors, selector=next_selector)
			i += 1

def main():
	if len(sys.argv) != 2:
		print('please include the path of the html file as an arg')
		return
	generate_css(sys.argv[1])

if __name__ == '__main__':
	main()
