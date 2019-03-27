from microbit import *
import utime
import microbit

unsigned = Image("90009:90009:90009:90009:09990")
signed = Image("99999:00900:00900:00900:99999")
floating = Image("09990:09000:09900:09000:09000")
character = Image("09999:90000:90000:90000:09999")
all_types = [unsigned, signed, floating, character]

screen = 0
bit_on_intensity = 5
bit_off_intensity = 0
led_value = 0
bit_pattern = []
i = len(bit_pattern)
j = i - 24
bit_pattern_as_string = ''.join(bit_pattern)

blink_half_period = 500  # half a second
blink_value = 0
blink_ms = utime.ticks_ms()
current_led_value = 0  # off
hold_ms = 100000000  # hold threshold

while True:
    if screen == 0:
        check_ms = utime.ticks_ms()
        if utime.ticks_diff(check_ms, blink_ms) >= blink_half_period:
            blink_ms = check_ms
            blink_value = (blink_value + 1) % 2
            if blink_value:
                if i < 25:
                    display.set_pixel(i % 5, i // 5, 9)
                else:
                    display.set_pixel(j % 5, j // 5, 9)
            elif current_led_value:
                if i < 25:
                    display.set_pixel(i % 5, i // 5, bit_on_intensity)
                else:
                    display.set_pixel(j % 5, j // 5, bit_on_intensity)
            else:
                if i < 25:
                    display.set_pixel(i % 5, i // 5, 0)
                else:
                    display.set_pixel(j % 5, j // 5, 0)

            if button_a.was_pressed():
                led_value = (current_led_value + 1) % 2  # alternating: if 1, then 0; if 0, then 1
                current_led_value = led_value
                if led_value > 0:
                    if i < 25:
                        display.set_pixel(i % 5, i // 5, bit_on_intensity)
                    else:
                        display.set_pixel(j % 5, j // 5, bit_on_intensity)
                if led_value == 0:
                    if i < 25:
                        display.set_pixel(i % 5, i // 5, 0)
                    else:
                        display.set_pixel(j % 5, j // 5, 0)

            if button_b.is_pressed():
                start_ms = utime.ticks_ms()
                while True:
                    if button_b.is_pressed():
                        break
                if utime.ticks_diff(utime.ticks_ms(), start_ms) < hold_ms and led_value == 1:
                    # simple press
                    if i < 25:
                        display.set_pixel(i % 5, i // 5, bit_on_intensity)
                    else:
                        display.set_pixel(j % 5, j // 5, bit_on_intensity)
                    bit_pattern.append('1')
                    i = len(bit_pattern)
                    j = i - 25
                    if j == 0:
                        microbit.display.clear()
                if utime.ticks_diff(utime.ticks_ms(), start_ms) < hold_ms and led_value != 1:
                    if i < 25:
                        display.set_pixel(i % 5, i // 5, 0)
                    else:
                        display.set_pixel(j % 5, j // 5, 0)
                    bit_pattern.append('0')
                    i = len(bit_pattern)
                    j = i - 25
                    if j == 0:
                        microbit.display.clear()
                if i == 32:
                        screen = (screen + 1) % 2

    if screen == 1:
        microbit.display.clear()
        display.show(all_types)
        display.show(Image.ARROW_E)
        d = -1
        while True:
            if button_a.was_pressed():
                d = (d + 1) % 4
                if d == 0:
                    display.show(unsigned)
                if d == 1:
                    display.show(signed)
                if d == 2:
                    display.show(floating)
                if d == 3:
                    display.show(character)
            if button_b.was_pressed():
                if d == 0:
                    display.scroll(int(''.join(str(i) for i in bit_pattern)))
                    display.show(unsigned)
                if d == 1:
                    display.scroll("Unimplemented")
                    display.show(signed)
                if d == 2:
                    display.scroll("Unimplemented")
                    display.show(floating)
                if d == 3:
                    display.scroll("Unimplemented")
                    display.show(character)