
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Speech.Recognition;
using System.Speech.Synthesis;

namespace StartingWithSpeechRecognition
{
    class Program
    {
        static SpeechRecognitionEngine _recognizer = null;
        static ManualResetEvent manualResetEvent = null;
        static Socket sender0 = null;
        static void Main(string[] args)
        {

            if (args.Length > 0)
            {
                string ip = args[0];
                int port = 5000;
                port = Convert.ToInt16(args[1]);

                try
                {
                    // Establish the remote endpoint for the socket.
                    // This example uses port 11000 on the local computer.
                    IPAddress ipAddress = IPAddress.Parse(ip);
                    IPEndPoint remoteEP = new IPEndPoint(ipAddress, port);

                    // Create a TCP/IP  socket.
                    sender0 = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

                    // Connect the socket to the remote endpoint. Catch any errors.
                    try
                    {
                        sender0.Connect(remoteEP);

                        Console.WriteLine("Conectados a {0}", sender0.RemoteEndPoint.ToString());
                        // Encode the data string into a byte array.
                    }
                    catch (ArgumentNullException ane)
                    {
                        Console.WriteLine("ArgumentNullException : {0}", ane.ToString());
                    }
                    catch (SocketException se)
                    {
                        Console.WriteLine("SocketException : {0}", se.ToString());
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Unexpected exception : {0}", e.ToString());
                    }

                }
                catch (Exception e)
                {
                    Console.WriteLine(e.ToString());
                }

            }


            manualResetEvent = new ManualResetEvent(false);
            Console.WriteLine("Reconocedor básico");
            RecognizeSpeechAndWriteToConsole();
            Console.WriteLine("Continuando reconocimiento");
            Console.ReadKey(true);


        }
        #region Recognize speech and write to console
        static void RecognizeSpeechAndWriteToConsole()
        {
            // Select a speech recognizer that supports English.
            RecognizerInfo info = null;
            Console.WriteLine("Reconocedores disponibles:");
            foreach (RecognizerInfo ri in SpeechRecognitionEngine.InstalledRecognizers())
            {
                Console.WriteLine(ri.Culture.TwoLetterISOLanguageName);
                if (ri.Culture.TwoLetterISOLanguageName.Equals("es"))
                {
                    info = ri;
                    break;
                }
            }
            if (info == null) return;

            _recognizer = new SpeechRecognitionEngine(info);
            _recognizer.LoadGrammar(CreateGrammar()); // "test" grammar
            _recognizer.SpeechRecognized += _recognizeSpeechAndWriteToConsole_SpeechRecognized; // if speech is recognized, call the specified method
            _recognizer.SpeechRecognitionRejected += _recognizeSpeechAndWriteToConsole_SpeechRecognitionRejected; // if recognized speech is rejected, call the specified method
            _recognizer.SetInputToDefaultAudioDevice(); // set the input to the default audio device
            _recognizer.RecognizeAsync(RecognizeMode.Multiple); // recognize speech asynchronous

        }
        static void _recognizeSpeechAndWriteToConsole_SpeechRecognized(object sender, SpeechRecognizedEventArgs e)
        {
            if (e.Result.Text == "salir")
            {
                manualResetEvent.Set();
                if (sender0 != null)
                {
                    sender0.Shutdown(SocketShutdown.Both);
                    sender0.Close();
                }
            }
            else
            {
                if (sender0 != null)
                {
                    try
                    {
                        // Encode the data string into a byte array.
                        byte[] msg = Encoding.ASCII.GetBytes(e.Result.Text);

                        // Send the data through the socket.
                        int bytesSent = sender0.Send(msg);

                        // Release the socket.
                    }
                    catch (ArgumentNullException ane)
                    {
                        Console.WriteLine("ArgumentNullException : {0}", ane.ToString());
                    }
                    catch (SocketException se)
                    {
                        Console.WriteLine("SocketException : {0}", se.ToString());
                    }
                    catch (Exception ee)
                    {
                        Console.WriteLine("Unexpected exception : {0}", ee.ToString());
                    }

                }
                Console.WriteLine(e.Result.Text);

            }
        }
        static void _recognizeSpeechAndWriteToConsole_SpeechRecognitionRejected(object sender, SpeechRecognitionRejectedEventArgs e)
        {
            Console.WriteLine("Comando rechazado. Dijiste:");
            foreach (RecognizedPhrase r in e.Result.Alternates)
            {
                Console.WriteLine("    " + r.Text);
            }
        }

        private static Grammar CreateGrammar()
        {

            // Create a Choices object with alternatives for toppings.
            Choices toppings = new Choices(new string[] {
                "bypass", 
                "aceptar", 
                "adquirir para adquisision", 
                "pausar adquisision",
                "grabar",
                "pausar",
                "reproducir",
                "detener",
                "seleccion uno",
                "seleccion dos",
                "seleccion tres",
                "seleccion cuatro",
                "nuevo bypass",
                "nueva medicion",
                "siguiente medicion",
                "anterior medicion"
            });

            // Create a GrammarBuilder and append the Choices object.
            GrammarBuilder gb = new GrammarBuilder(toppings, 0, 1);

            // Create the Grammar from the GrammarBuilder.
            Grammar grammar = new Grammar(gb);
            grammar.Name = "Commandos";

            return grammar;
        }
        #endregion
    }
}
