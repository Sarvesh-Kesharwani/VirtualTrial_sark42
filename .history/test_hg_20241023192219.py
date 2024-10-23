from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("yisol/IDM-VTON")
prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
image = pipe(prompt).images[0]
DOWNLOAD_PATH: Final = './downloads/'  # Define a directory to save images