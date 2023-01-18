import pandas as pd
import numpy as np
import time
import random
import os
from faker import Faker
from super_market import SuperMarket, Sections
from tiles_skeleton import SupermarketMap, MARKET
from customer import Customer
import cv2
from argparse import ArgumentParser

parser = ArgumentParser(
    prog='Supermarket simulation', 
    description='Creates a visualization of customer in a supermarket'
)

parser.add_argument(
    "-g", 
    "--gif", 
    dest="save_gif",
    action='store_true',
    help="Set to true and the program will output a gif to the artifacts folder", 
    default=False
)

parser.add_argument(
    "-t", 
    "--sim-time", 
    dest="min_sec_time_simulation",
    help="How long a minute is when running the simulation", 
    type=int, 
    default=1
)

parser.add_argument(
    "-s", 
    "--start-date", 
    dest="start_date",
    help="The start date of the simulation", 
    type=str, 
    default='01-03-2017'
)

parser.add_argument(
    "-e", 
    "--end-date", 
    dest="end_date",
    help="The end date of the simulation", 
    type=str, 
    default='1-1-2018'
)

parser.add_argument(
    "-f", 
    "--fps", 
    dest="fps",
    help="How many frames per second for the animation", 
    type=int, 
    default=3
)

args = vars(parser.parse_args())
print('Args: ', args)

save_gif = args['save_gif']
min_sec_time_simulation = args['min_sec_time_simulation']
start_date = args['start_date']
end_date = args['end_date']
fps = args['fps']

directory = os.path.dirname(os.path.realpath(__file__))

if save_gif:
    from os import listdir
    from os.path import isfile, join
    
    frames_path = f'{directory}/artifacts/frames/'
    isExist = os.path.exists(frames_path)
    if not isExist:
        # Create a new directory if it does not exist
        os.makedirs(frames_path)
    else:
        # Delete existing directory contents
        for file in os.listdir(frames_path):
            os.remove(f'{frames_path}{file}')   

next_locations_df = pd.read_csv(f'{directory}/data/customer_transitions.csv')

P = pd.crosstab(
    next_locations_df['location'],
    next_locations_df['next_location'], normalize='index')

probs_dict = P.to_dict(orient='index')

probs = {}

for key in probs_dict.keys():
    probs[key] = list(probs_dict[key].values())

faker = Faker()

date_range = pd.date_range(start =start_date, 
            end =end_date, freq = '1min')

background = np.zeros((500, 700, 3), np.uint8)

tiles = cv2.imread(f"{directory}/tiles.png")

sections = Sections(
    ## First index is how far down
    ## Second index is how far across
    entrance=[(10, 14),(10, 15)],
    exit=[(10, 14)],
    dairy=[(2, 3), (3, 3), (4, 3), (5, 3), (6, 3)],
    spices=[( 2, 7), ( 3, 7), ( 4, 7), ( 5, 7), ( 6, 7)],
    drinks=[(7, 16),(8, 16),(9, 16)],
    fruit=[(2, 14), (3, 14), (4, 14), (5, 14), (6, 14)],
    checkout=[(8, 3), (8, 7), (8, 11)],
)

supermarket_map = SupermarketMap(MARKET, tiles)

supermarket = SuperMarket('Quick STOP Groceries', P, supermarket_map, sections)

customer_amount_in_store_df = pd.read_csv(f'{directory}/data/amount_of_customers_at_time.csv', index_col=0, parse_dates=True)
customer_amount_in_store_df = customer_amount_in_store_df.groupby([ 'day', 'hour', 'minute' ]).mean()
        

for date_time_minute in date_range:
    
    day = date_time_minute.day_name()
    hour = date_time_minute.hour
    minute = date_time_minute.minute

    new_customer_amount = 0
    total_visits = supermarket.get_total_customer_count()
    
    if hour >= 7 and minute > 5:
        try:
            max_customers = customer_amount_in_store_df.loc[day, hour, minute]['customer_no']  # type: ignore
            current_customer_count = supermarket.get_customer_count()
            new_customer_amount = 0 if max_customers < current_customer_count else max_customers - current_customer_count
        except:
            print('Could not find data from customers at day, hour, minute', day, hour, minute)
            pass
    
    entrance_location = sections.get_location_from_state('entrance')
    
    supermarket.add_customers([
            Customer(str(f'{faker.name()} ID:{i}'), supermarket.map, str(random.randint(1,17)),entrance_location[0], entrance_location[1] )
            for i
                in range(
                        total_visits + 1,
                        random.randint(
                                round(total_visits + 1 + new_customer_amount * 0.9),
                                round(total_visits + 1 + new_customer_amount * 1.1)
                            )
                    )
        ])
    
    print('Day:', day ,' - Hour: %s' % hour,' - Minute: %s' % minute, ' - Customer Count:', supermarket.get_customer_count(), ' - Total', total_visits )
    
    frame = background.copy()

    frame = supermarket.draw(frame)

    # https://www.ascii-code.com/
    key = cv2.waitKey(1)
    
        # Window name in which image is displayed
    window_name = f'"{supermarket.name}" - Time: {date_time_minute} - Customer_Count: {supermarket.get_customer_count()}'

    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    # org
    org = (8, 450)
    # fontScale
    fontScale = 0.5
    # Blue color in BGR
    color = (255, 200, 200)
    # Line thickness of 2 px
    thickness = 1
    # Using cv2.putText() method
    frame = cv2.putText(frame, window_name, org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
    
    cv2.imshow("frame", frame)
    
    if save_gif:
        writing_file = f'{directory}/artifacts/frames/{date_time_minute}.jpg'.replace(' ', '_')
        
        cv2.imwrite(writing_file, frame)

    customer_states = supermarket.tick_minute()
    
    if (hour > 6) and (hour < 22):
        time.sleep(min_sec_time_simulation)
    else:
        print('Speeding up time')


cv2.destroyAllWindows()

supermarket.map.write_image("supermarket.png")

if save_gif:
    import imageio

    images_dir = f'{directory}/artifacts/frames/'
    animations_path = f'{directory}/artifacts/animations/'
    if not os.path.exists(animations_path):
        os.makedirs(animations_path)
    
    images = []
    
    for filename in [f for f in listdir(images_dir) if isfile(join(images_dir, f))]:
        images.append(imageio.imread(f'{images_dir}{filename}'))

   
    imageio.mimsave(f'{animations_path}output.gif', images, fps=fps)