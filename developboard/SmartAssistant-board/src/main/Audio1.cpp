#include <ArduinoJson.h>
#include <cmath>
#include "Audio1.h"

Audio1::Audio1()
{
  // Initialize member variables and allocate memory as necessary
  wavData = nullptr;
  i2s = new I2S();
}

Audio1::~Audio1()
{
  // Free dynamically allocated memory
  for (int i = 0; i < wavDataSize / dividedWavDataSize; ++i)
    delete[] wavData[i];
  delete[] wavData;
  delete i2s;
}

void Audio1::init()
{
  // Allocate memory for WAV data
  wavData = new char *[1];
  for (int i = 0; i < 1; ++i)
    wavData[i] = new char[1280];
}

void Audio1::clear()
{
  // Clear the I2S buffer
  i2s->clear();
}

void Audio1::CreateWavHeader(byte *header, int waveDataSize)
{
  // Create a WAV header for mono, 16-bit PCM audio at 16,000 Hz
  header[0] = 'R'; header[1] = 'I'; header[2] = 'F'; header[3] = 'F';
  unsigned int fileSizeMinus8 = waveDataSize + 44 - 8;
  header[4] = (byte)(fileSizeMinus8 & 0xFF);
  header[5] = (byte)((fileSizeMinus8 >> 8) & 0xFF);
  header[6] = (byte)((fileSizeMinus8 >> 16) & 0xFF);
  header[7] = (byte)((fileSizeMinus8 >> 24) & 0xFF);
  header[8] = 'W'; header[9] = 'A'; header[10] = 'V'; header[11] = 'E';
  header[12] = 'f'; header[13] = 'm'; header[14] = 't'; header[15] = ' ';
  header[16] = 0x10; header[17] = 0x00; header[18] = 0x00; header[19] = 0x00;
  header[20] = 0x01; header[21] = 0x00;
  header[22] = 0x01; header[23] = 0x00; // Mono audio
  header[24] = 0x80; header[25] = 0x3E; // Sampling rate 16000 Hz
  header[28] = 0x00; header[29] = 0x7D; // Byte rate 32000 bytes/sec
  header[32] = 0x02; header[33] = 0x00; // 16-bit mono
  header[36] = 'd'; header[37] = 'a'; header[38] = 't'; header[39] = 'a';
  header[40] = (byte)(waveDataSize & 0xFF);
  header[41] = (byte)((waveDataSize >> 8) & 0xFF);
  header[42] = (byte)((waveDataSize >> 16) & 0xFF);
  header[43] = (byte)((waveDataSize >> 24) & 0xFF);
}

void Audio1::Record()
{
  // Read audio data from I2S buffer
  i2s->Read(i2sBuffer, i2sBufferSize);
  for (int i = 0; i < i2sBufferSize / 8; ++i)
  {
    wavData[0][2 * i] = i2sBuffer[8 * i + 2];
    wavData[0][2 * i + 1] = i2sBuffer[8 * i + 3];
  }
}

String Audio1::parseJSON(const char *jsonResponse)
{
  DynamicJsonDocument doc(1024);

  // Parse the JSON response
  DeserializationError error = deserializeJson(doc, jsonResponse);
  if (error)
  {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.f_str());
    return String("");
  }

  // Extract and return the "question" field
  const char *question = doc["result"][0];
  return String(question);
}

float Audio1::calculateRMS(uint8_t *buffer, int bufferSize)
{
  float sum = 0;
  int16_t sample;

  // Process every two bytes as a 16-bit sample
  for (int i = 0; i < bufferSize; i += 2)
  {
    sample = (buffer[i + 1] << 8) | buffer[i]; // Convert to 16-bit sample
    sum += sample * sample; // Accumulate square of the sample
  }

  // Calculate the mean square
  sum /= (bufferSize / 2);

  // Return the RMS value
  return sqrt(sum);
}
