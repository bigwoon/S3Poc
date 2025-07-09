import React, { useState } from 'react';
import { View, Text, TextInput, Button, ActivityIndicator, StyleSheet, Alert } from 'react-native';
import * as ExpoAV from 'expo-av';

export default function IndexScreen() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [fileUrl, setFileUrl] = useState<string | null>(null);
  const [soundObj, setSoundObj] = useState<ExpoAV.Audio.Sound | null>(null);

  const generateAudio = async () => {
    if (!prompt.trim()) {
      Alert.alert('Error', 'Prompt cannot be empty.');
      return;
    }

    setLoading(true);
    setFileUrl(null);

    try {
      const response = await fetch('http://localhost:8000/generate-audio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: prompt }),
      });

      const data = await response.json();
      if (data.success) {
        setFileUrl(data.file_url);
        await playAudio(data.file_url);
      } else {
        Alert.alert('Error', data.error || 'Audio generation failed');
      }
    } catch (error) {
      console.error('❌ Fetch error:', error);
      Alert.alert('Error', 'Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const playAudio = async (url: string) => {
    try {
      if (soundObj) {
        await soundObj.unloadAsync();
      }
      const { sound } = await ExpoAV.Audio.Sound.createAsync({ uri: url });
      setSoundObj(sound);
      await sound.playAsync();
    } catch (error) {
      console.error('🔇 Playback error:', error);
      Alert.alert('Error', 'Could not play the audio');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>NRVE Audio Generator 🎶</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter music prompt..."
        value={prompt}
        onChangeText={setPrompt}
      />
      <Button title="Generate Audio" onPress={generateAudio} disabled={loading} />
      {loading && <ActivityIndicator style={{ marginTop: 20 }} size="large" color="#6200ee" />}
      {fileUrl && (
        <Text style={styles.url}>Audio URL: {fileUrl}</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 24,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    borderColor: '#ccc',
    borderWidth: 1,
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
    backgroundColor: '#fff',
  },
  url: {
    marginTop: 24,
    fontSize: 12,
    color: 'blue',
  },
});

