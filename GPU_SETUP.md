# Использование GPU с NVIDIA

Для использования GPU от NVIDIA с этим ботом, следуйте этим шагам:

## Требования

- Видеокарта NVIDIA с поддержкой CUDA
- Установленные драйвера NVIDIA
- Установленная CUDA Toolkit (версия 11.8 или 12.1)

## Установка PyTorch с поддержкой CUDA

1. Удалите текущую версию PyTorch:
   ```bash
   pip uninstall torch torchvision torchaudio
   ```

2. Установите PyTorch с поддержкой CUDA:
   Для CUDA 11.8:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
   
   Для CUDA 12.1:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

3. Убедитесь, что PyTorch с CUDA установлен правильно:
   ```python
   import torch
   print(torch.cuda.is_available())  # Должно вернуть True
   print(torch.cuda.get_device_name(0))  # Покажет название вашей видеокарты
   ```

## Проверка использования GPU

Бот автоматически будет использовать GPU, если он доступен. В логах вы увидите сообщение:
```
Loading Whisper model (base) on cuda...
```

Если GPU недоступен, бот будет использовать CPU:
```
Loading Whisper model (base) on cpu...
```

## Производительность

Использование GPU значительно ускоряет процесс транскрибации:
- Модель large: ~6-8x быстрее на GPU чем на CPU
- Модель medium: ~3-4x быстрее на GPU чем на CPU
- Модель base: ~2-3x быстрее на GPU чем на CPU

## Устранение неполадок

Если PyTorch не использует GPU:
1. Проверьте, что драйвера NVIDIA установлены корректно
2. Убедитесь, что CUDA Toolkit совместима с вашей версией PyTorch
3. Проверьте, что у вас достаточно видеопамяти для выбранной модели Whisper