import RPi.GPIO as GPIO
import time

# Constants for GPIO pins
LED_PIN = 24       # GPIO pin for LED
SWITCH_PIN = 22    # GPIO pin for switch

def init_gpio():
    """Initialize GPIO settings for LED and switch."""
    GPIO.setmode(GPIO.BCM)  # Use Broadcom (BCM) pin numbering
    GPIO.setwarnings(False)
    GPIO.setup(LED_PIN, GPIO.OUT)  # Set GPIO 24 as output for LED
    GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set GPIO 22 as input with pull-up

def main():
    init_gpio()  # Initialize GPIO pins

    led_on = False            # LED state
    last_toggle_time = time.time()  # Last toggle time for LED
    blink_frequency = 5       # Default blink frequency in Hz
    duration_timer = None     # Timer for the 10 Hz, 5-second duration
    blinking_active = True    # Flag to manage whether blinking is active

    try:
        while True:
            switch_position = GPIO.input(SWITCH_PIN)  # Read the switch position

            # Left position (LOW): 5 Hz continuous blinking
            if switch_position == GPIO.LOW:
                if duration_timer:  # Reset the 10 Hz timer if it was set
                    duration_timer = None
                blink_frequency = 5  # Set blink frequency to 5 Hz
                blinking_active = True  # Enable continuous blinking

            # Right position (HIGH): 10 Hz blinking for 5 seconds
            elif switch_position == GPIO.HIGH:
                if not duration_timer:  # Only start the duration timer if not already running
                    duration_timer = time.time()  # Start the 5-second timer
                blink_frequency = 10  # Set blink frequency to 10 Hz

                # Stop blinking after 5 seconds
                if time.time() - duration_timer >= 5:
                    GPIO.output(LED_PIN, GPIO.LOW)  # Turn off the LED
                    blinking_active = False  # Disable blinking
                else:
                    blinking_active = True  # Keep blinking if within 5 seconds

            # Handle LED blinking at the set frequency
            current_time = time.time()
            if blinking_active and (current_time - last_toggle_time) >= (1 / (2 * blink_frequency)):
                led_on = not led_on
                GPIO.output(LED_PIN, led_on)
                last_toggle_time = current_time

            time.sleep(0.01)  # Small delay to prevent excessive CPU usage

    except KeyboardInterrupt:
        pass  # Allow clean exit on CTRL+C

    finally:
        GPIO.cleanup()  # Reset GPIO pins on exit

if __name__ == "__main__":
    main()
