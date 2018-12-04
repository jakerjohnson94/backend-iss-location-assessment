#!/usr/bin/env python
import turtle               # allows us to use the turtles library
import requests
import time

__author__ = 'Jake Johnson'


INDY_COORDS = (40.267193, -86.134903)


def draw_map(lat, long):
    iss_turtle = turtle.Turtle()
    screen = turtle.Screen()
    screen.setup(height=360, width=720)
    screen.setworldcoordinates(90.0, 180.0, -90.0, -180.0,)
    screen.bgpic('map.gif')
    screen.register_shape("iss.gif")
    draw_passover_info(iss_turtle, *INDY_COORDS)
    draw_iss(iss_turtle, lat, long)
    turtle.mainloop()


def draw_iss(iss_turtle, lat, long):
    iss_turtle.shape('iss.gif')
    iss_turtle.penup()
    iss_turtle.goto(float(lat), float(long))
    iss_turtle.pendown()


def draw_passover_info(iss_turtle, *coords):
    data = requests.get(
        'http://api.open-notify.org/iss-pass.json?lat={}&lon={}'
        .format(*coords)).json()
    timestamp = time.ctime(data['response'][0]['risetime'])
    iss_turtle.penup()
    iss_turtle.goto(*coords)
    iss_turtle.dot(5, 'yellow')
    iss_turtle.color('white')
    iss_turtle.write(timestamp)


def get_iss_info(url):
    data = requests.get(url).json()
    position = data['iss_position']
    timestamp = data['timestamp']
    lat = position['latitude'].encode('utf8')
    long = position['longitude'].encode('utf8')

    return (timestamp, lat, long)


def print_iss_info(timestamp, lat, long):
    print('\nCurrent Time: ' + time.ctime(timestamp))
    print('Latitude ' + str(lat))
    print('Longitude: ' + str(long))


def get_austronauts(url):

    data = requests.get(url).json()
    num = data['number']
    people = data['people']

    # format values in response objects to utf8 and extract values for printing
    people = [[b''.join([z.encode('utf8') for z in y])
               for y in x.values()] for x in people]

    return (num, people)


def print_astronauts(num, people):
    print('{} total people in space:\n').format(num)
    print('Name: {} Spacecraft:').format(' '*10)
    for craft, name in people:
        print('{} - {}').format(name, craft)


def main():

    urls = {'astro': 'http://api.open-notify.org/astros.json',
            'iss': 'http://api.open-notify.org/iss-now.json',
            }
    num, people = get_austronauts(urls['astro'])
    timestamp, lat, long = get_iss_info(urls['iss'])
    print_astronauts(num, people)
    print_iss_info(timestamp, lat, long)
    draw_map(lat, long)


if __name__ == '__main__':
    main()
