from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

def generate_reply(comment, sentiment):
    # Define strict prompts to reduce randomness
    if sentiment.lower() == "negative":
        prompt = (
            f"You are a brand replying politely to a negative Instagram comment. "
            f"Reply briefly with empathy and professionalism, avoiding emojis, usernames, or casual language.\n"
            f"Comment: {comment}\n"
            f"Reply:"
        )
        max_tokens = 25

    elif sentiment.lower() == "positive":
        prompt = (
            f"You are a brand replying warmly to a positive Instagram comment. "
            f"Reply briefly with gratitude and professionalism. Avoid emojis, usernames, or overly casual words.\n"
            f"Comment: {comment}\n"
            f"Reply:"
        )
        max_tokens = 25

    else:
        prompt = (
            f"You are a brand replying professionally to an Instagram comment. "
            f"Reply briefly in a polite and brand-safe tone. Do not include usernames or emojis.\n"
            f"Comment: {comment}\n"
            f"Reply:"
        )
        max_tokens = 25

    # Generate reply
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.1,
        do_sample=True
    )

    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Post-cleanup
    if "Reply:" in reply:
        reply = reply.split("Reply:")[-1].strip()

    # Remove AI hallucinated usernames or garbage
    if reply.startswith("@") or "@" in reply:
        reply = reply.replace("@", "").strip(" -")

    # Fallback replies for low-quality output
    if len(reply) < 3 or not any(c.isalpha() for c in reply):
        if sentiment.lower() == "negative":
            reply = "Sorry to hear that. We’ll work on it."
        elif sentiment.lower() == "positive":
            reply = "Thanks a lot! We appreciate your support."
        else:
            reply = "Thank you! We value your feedback."

    return reply
