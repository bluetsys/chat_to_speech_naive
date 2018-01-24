// C# SpeechSynthesizer [문서][1]에서 복붙
// 
// [1]: https://msdn.microsoft.com/en-us/library/system.speech.synthesis.speechsynthesizer(v=vs.110).aspx

using System;
using System.IO;
using System.Speech.Synthesis;

namespace SampleSynthesis
{
  class Program
  {
    static void Main(string[] args)
    {
      var text = args[0];

      SpeechSynthesizer synth = new SpeechSynthesizer();

      // TTS 한글 관련 문제 이걸로 정리.
      synth.SelectVoice("Microsoft Heami Desktop");

      // 구글에 "C# get random filename" 해서 나온 결과 C#의 이 [문서][2]가 나옴.
      // 
      // [2]: https://msdn.microsoft.com/en-us/library/system.io.path.getrandomfilename(v=vs.110).aspx
      string filename = Path.GetRandomFileName();

      // C#의 관련 [문서][3] 참고.
      // 
      // [3]: https://msdn.microsoft.com/en-us/library/ms586885(v=vs.110).aspx
      synth.SetOutputToWaveFile(@"D:\temp\" + filename +".wav");

      // SpeakAsync도 있고, text말고 Prompt, PromptBuilder를 사용한 것도 있지만 다 특별한 점은 모르겠으며,
      // SpeakAsync 사용시 파일이 재생 가능함에도 사이즈가 0KB로 보여서 불편,
      // Prompt, PromptBuilder로는 한국어 재생하기가 String (text 변수)만큼 쉽지가 않아서
      // 에러 몇번 받고 시도 조차 안함.
      synth.Speak(text);

      // Subprocess로 실행시 목소리 파일 생성시 사용된 파일이름을 출력,
      // Parent process에서는 파일 이름을 전달 받음.
      Console.Write(filename);
    }
  }
}