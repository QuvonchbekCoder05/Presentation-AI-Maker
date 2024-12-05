import openai


def generate_presentation_content(title, slides_count):
    openai.api_key = "OPENAI KEY"
    slides = []
    for i in range(slides_count):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Create slide {i+1} for a presentation about {title}",
            max_tokens=150,
        )
        slides.append(
            {
                "title": f"Slide {i+1}",
                "content": response.choices[0].text.strip(),
            }
        )
    return slides
