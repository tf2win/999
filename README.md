juni 2023 
The beginning of the code contains import statements to download the necessary packages and configure the environment for the Raspberry Pi.
Definition of GPIO connections for the seventh-party display and joystick for the numeric values on the display.
Definition of displayed digit points for digits on the hexadecimal display.
Definition of the number range that associates digits on the hexadecimal display with corresponding numbers in the num dictionary.
Definition of methods related to saving and processing of JSON files.
Definition of a method that retrieves data from Landsnet by making an HTTP request.
Definition of a method that controls the execution of displayed digits on the hexadecimal display with the help of the GPIO connections.
Definition of a method that runs the program and maintains updates to the data from Landsnet.
The main parts of the code:

fetch_landsnet_data(): This method fetches data from Landsnet by sending an HTTP request to their website. It uses the requests package to make the request and get the response as a JSON database. The response is saved in a better_data.json file with the help of the save_to_json() method. This method also performs calculations on the data displayed on the seventh-person display.
main(): This method runs the program and maintains updates of the data from Landsnet. It uses fetch_landsnet_data() to update the data and keeps a timestamp for the last update. If the data is older than 300 seconds, fetch_landsnet_data() is called to refresh the data. This method is in an infinite loop, so it will continue running without end.
To run the code, it is placed in the if __name__ == '__main__': block along with the `
