from PIL import Image
import random
import os

class DroneEncryptor:
    def __init__(self, key_seed, rows=10, cols=10):
        
        self.seed = key_seed
        self.rows = rows
        self.cols = cols

    def _generate_permutation_table(self, total_blocks):
        
        indices = list(range(total_blocks))
        random.seed(self.seed)
        random.shuffle(indices)
        return indices

    def process_image(self, image_path, mode='encrypt'):
        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            print("Файл не знайдено!")
            return None

        w, h = img.size
        
        block_w = w // self.cols
        block_h = h // self.rows
        
        blocks = []
        for r in range(self.rows):
            for c in range(self.cols):
                left = c * block_w
                upper = r * block_h
                right = left + block_w
                lower = upper + block_h
                
                blocks.append(img.crop((left, upper, right, lower)))

        total_blocks = len(blocks)
        
        perm_table = self._generate_permutation_table(total_blocks)
        
        new_img = Image.new('RGB', (w, h))
        
        if mode == 'encrypt':
            for i, original_block_idx in enumerate(perm_table):
                
                dest_r = i // self.cols
                dest_c = i % self.cols
                
                new_img.paste(blocks[original_block_idx], (dest_c * block_w, dest_r * block_h))
                
        elif mode == 'decrypt':
            restored_blocks = [None] * total_blocks
            
            for encrypted_pos, original_pos in enumerate(perm_table):
                restored_blocks[original_pos] = blocks[encrypted_pos]
           
            for i, block in enumerate(restored_blocks):
                r = i // self.cols
                c = i % self.cols
                new_img.paste(block, (c * block_w, r * block_h))

        return new_img

def main():

    input_file = "test_image.jpg" 
    secret_key = 123456           
 
    drone_security = DroneEncryptor(key_seed=secret_key, rows=10, cols=10)
    
    print(f"1. Шифруємо файл: {input_file}...")
    encrypted_img = drone_security.process_image(input_file, mode='encrypt')
    
    if encrypted_img:
        encrypted_img.save("encrypted.png")
        print("   Готово! Збережено як 'encrypted.png'")
        
        print("2. Розшифровуємо назад...")
        decrypted_img = drone_security.process_image("encrypted.png", mode='decrypt')
        decrypted_img.save("decrypted.png")
        print("   Готово! Збережено як 'decrypted.png'")

if __name__ == "__main__":
    if not os.path.exists("test_image.jpg"):
        img = Image.new('RGB', (400, 300), color = 'red')
        img.save("test_image.jpg")
        
    main()
