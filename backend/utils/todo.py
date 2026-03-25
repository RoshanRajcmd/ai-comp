def execute_action_and_get_result(self, action_data):
    raw_action = action_data.get("action", "").lower().strip()
    value = action_data.get("value") or action_data.get("query")

    VALID_TOOLS = {
        "get_time", "search_web", "capture_image"
    }

    ALIASES = {
        "google": "search_web", "browser": "search_web", "news": "search_web",
        "search_news": "search_web", "look": "capture_image", "see": "capture_image",
        "check_time": "get_time"
    }

    action = ALIASES.get(raw_action, raw_action)
    print(f"ACTION: {raw_action} -> {action}", flush=True)

    if action not in VALID_TOOLS:
        if value and isinstance(value, str) and len(value.split()) > 1:
            return f"CHAT_FALLBACK::{value}"
        return "INVALID_ACTION"

    if action == "get_time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    elif action == "search_web":
        print(f"Searching web for: {value}...", flush=True)
        try:
            # 'us-en' region is often more stable for CLI queries
            with DDGS() as ddgs:
                results = []
                # 1. News search
                try:
                    results = list(ddgs.news(value, region='us-en', max_results=1))
                    if results:
                        print(f"[DEBUG] Found News: {results[0].get('title')}", flush=True)
                except Exception as e:
                    print(f"[DEBUG] News Search Error: {e}", flush=True)

                # 2. Text fallback
                if not results:
                    print("[DEBUG] No news found, trying text search...", flush=True)
                    try:
                        results = list(ddgs.text(value, region='us-en', max_results=1))
                        if results:
                            print(f"[DEBUG] Found Text: {results[0].get('title')}", flush=True)
                    except Exception as e:
                        print(f"[DEBUG] Text Search Error: {e}", flush=True)

                if results:
                    r = results[0]
                    # Safe get
                    title = r.get('title', 'No Title')
                    body = r.get('body', r.get('snippet', 'No Body'))
                    return f"SEARCH RESULTS for '{value}':\nTitle: {title}\nSnippet: {body[:300]}"
                else:
                    print(f"[DEBUG] Search returned 0 results.", flush=True)
                    return "SEARCH_EMPTY"
        except Exception as e:
            print(f"[DEBUG] Connection/Library Error: {e}", flush=True)
            return "SEARCH_ERROR"

    elif action == "capture_image":
        return "IMAGE_CAPTURE_TRIGGERED"

    return None

# =========================================================================
# 4. CORE LOGIC
# =========================================================================


def warm_up_logic(self):
    self.set_state(BotStates.WARMUP, "Warming up brains...")
    try:
        ollama.generate(model=TEXT_MODEL, prompt="", keep_alive=-1)
    except Exception as e:
        print(f"Failed to load {TEXT_MODEL}: {e}", flush=True)
    self.play_sound(self.get_random_sound(greeting_sounds_dir))
    print("Models loaded.", flush=True)

def chat_and_respond(self, text, img_path=None):
    if "forget everything" in text.lower() or "reset memory" in text.lower():
        self.session_memory = []
        self.permanent_memory = [{"role": "assistant", "content": SYSTEM_PROMPT}]
        self.save_chat_history()
        with self.tts_queue_lock:
            self.tts_queue.append("Okay. Memory wiped.")
        self.set_state(BotStates.IDLE, "Memory Wiped")
        return

    model_to_use = VISION_MODEL if img_path else TEXT_MODEL
    self.set_state(BotStates.THINKING, "Thinking...", cam_path=img_path)

    messages = []
    if img_path:
        messages = [{"role": "user", "content": text, "images": [img_path]}]
    else:
        user_msg = {"role": "user", "content": text}
        messages = self.permanent_memory + self.session_memory + [user_msg]

    self.thinking_sound_active.set()
    threading.Thread(target=self._run_thinking_sound_loop, daemon=True).start()

    full_response_buffer = ""
    sentence_buffer = ""

    try:
        stream = ollama.chat(model=model_to_use, messages=messages, stream=True, options=OLLAMA_OPTIONS)

        is_action_mode = False

        for chunk in stream:
            if self.interrupted.is_set(): break
            content = chunk['message']['content']
            full_response_buffer += content

            if '{"' in content or "action:" in content.lower():
                is_action_mode = True
                self.thinking_sound_active.clear()
                continue

            if is_action_mode: continue

            self.thinking_sound_active.clear()
            if self.current_state != BotStates.SPEAKING:
                self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)
                self.append_to_text("BOT: ", newline=False)

            self._stream_to_text(content)

            sentence_buffer += content
            if any(punct in content for punct in ".!?\n"):
                clean_sentence = sentence_buffer.strip()
                if clean_sentence and re.search(r'[a-zA-Z0-9]', clean_sentence):
                    with self.tts_queue_lock: self.tts_queue.append(clean_sentence)
                sentence_buffer = ""

        if is_action_mode:
            action_data = self.extract_json_from_text(full_response_buffer)
            if action_data:
                tool_result = self.execute_action_and_get_result(action_data)

                if tool_result and tool_result.startswith("CHAT_FALLBACK::"):
                    chat_text = tool_result.split("::", 1)[1]
                    self.thinking_sound_active.clear()
                    self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)
                    self.append_to_text("BOT: ", newline=False)
                    self.append_to_text(chat_text, newline=True)
                    with self.tts_queue_lock: self.tts_queue.append(chat_text)
                    self.session_memory.append({"role": "assistant", "content": chat_text})
                    self.wait_for_tts()
                    self.set_state(BotStates.IDLE, "Ready")
                    return

                if tool_result == "IMAGE_CAPTURE_TRIGGERED":
                    new_img_path = self.capture_image()
                    if new_img_path:
                        self.chat_and_respond(text, img_path=new_img_path)
                        return

                elif tool_result == "INVALID_ACTION":
                    fallback_text = "I am not sure how to do that."
                    self.thinking_sound_active.clear()
                    self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)
                    self.append_to_text("BOT: ", newline=False)
                    self.append_to_text(fallback_text, newline=True)
                    with self.tts_queue_lock: self.tts_queue.append(fallback_text)

                elif tool_result == "SEARCH_EMPTY":
                    fallback_text = "I searched, but I couldn't find any news about that."
                    self.thinking_sound_active.clear()
                    self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)
                    self.append_to_text("BOT: ", newline=False)
                    self.append_to_text(fallback_text, newline=True)
                    with self.tts_queue_lock: self.tts_queue.append(fallback_text)

                elif tool_result == "SEARCH_ERROR":
                    fallback_text = "I cannot reach the internet right now."
                    self.thinking_sound_active.clear()
                    self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)
                    self.append_to_text("BOT: ", newline=False)
                    self.append_to_text(fallback_text, newline=True)
                    with self.tts_queue_lock: self.tts_queue.append(fallback_text)

                elif tool_result:
                    summary_prompt = [
                        {"role": "assistant", "content": "Summarize this result in one short sentence."},
                        {"role": "user", "content": f"RESULT: {tool_result}\nUser Question: {text}"}
                    ]

                    self.set_state(BotStates.THINKING, "Reading...")
                    self.thinking_sound_active.set()

                    final_resp = ollama.chat(model=model_to_use, messages=summary_prompt, stream=False, options=OLLAMA_OPTIONS)
                    final_text = final_resp['message']['content']

                    self.thinking_sound_active.clear()
                    self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)

                    self.append_to_text("BOT: ", newline=False)
                    self.append_to_text(final_text, newline=True)
                    with self.tts_queue_lock: self.tts_queue.append(final_text)
                    self.session_memory.append({"role": "assistant", "content": final_text})
        else:
            self.append_to_text("")
            self.session_memory.append({"role": "assistant", "content": full_response_buffer})

        self.wait_for_tts()
        self.set_state(BotStates.IDLE, "Ready")

    except Exception as e:
        print(f"LLM Error: {e}")
        self.set_state(BotStates.ERROR, "Brain Freeze!")