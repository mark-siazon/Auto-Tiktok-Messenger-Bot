import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from core.browser import init_browser
from core.utils import human_delay, type_like_human
from core.user_tracker import has_already_messaged, save_messaged_user
from core.message_gen import generate_human_message
from tkinter import messagebox

def start_bot():
    # Start browser session
    browser, wait = init_browser()

    try:
        print("🧭 Navigating to TikTok Messages")
        browser.get("https://www.tiktok.com/messages")
        human_delay(5, 7)

        # Find all users in the chat list
        chat_boxes = wait.until(lambda d: d.find_elements(By.XPATH, "//div[@data-e2e='chat-list-item']"))
        print(f"🔍 Found {len(chat_boxes)} user(s) in the chat list")

        for user in chat_boxes:
            try:
                # Click each user in the sidebar
                browser.execute_script("arguments[0].scrollIntoView();", user)
                user.click()
                human_delay(3, 5)

                # Get username from chat header
                username_element = wait.until(lambda d: d.find_element(By.CLASS_NAME, "css-16y88xx-PInfoNickname"))
                username = username_element.text.strip()

                # Skip if already messaged recently
                if has_already_messaged(username):
                    print(f"⏩ Skipped @{username} (already messaged recently)")
                    continue

                # Wait for message input box
                message_box = wait.until(lambda d: d.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block"))
                message_box.click()

                # Generate and send the message
                auto_msg = generate_human_message()
                print(f"✉️ Sending to @{username}: {auto_msg}")
                type_like_human(message_box, auto_msg)
                message_box.send_keys(Keys.RETURN)

                # Log the message
                save_messaged_user(username)
                print(f"✅ Message sent to @{username}")
                human_delay(5, 7)

            except Exception as e:
                print("⚠️ Failed to send message:", e)
                browser.save_screenshot(f"fail_{random.randint(1000,9999)}.png")
                continue

    except Exception as e:
        print("Critical Error:", e)
        browser.save_screenshot("critical_error.png")

    finally:
        browser.quit()
        messagebox.showinfo("Done", "Messages sent (or attempted).")
