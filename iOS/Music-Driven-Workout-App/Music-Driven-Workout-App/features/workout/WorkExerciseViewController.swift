//
//  WorkExerciseViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class WorkExerciseViewController: UIViewController, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {
    
    var auth = SPTAuth.defaultInstance()!
    var heartrate = 0
    
    //variables to be taken from workout summary
    var workoutjson: String!
    var exercisenames: [String]!
    var exercisedescriptions: [String]!
    var exercisedurations: [Int]!
    var exerciseimages: [String]!
    var exercisetracknames: [[String]]!
    var exercisetrackuris: [[String]]!
    var session:SPTSession!
    var player: SPTAudioStreamingController?
    var queued = false
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        heartratelabel.adjustsFontSizeToFitWidth = true
        initSpotify()
        startWorkout()
        //self.player = GlobalVariables.sharedManager.player
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /* MARK: - Navigation */
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        present(vc, animated: true, completion: nil)
    }
    
    //ui elements
    @IBOutlet weak var quitbutton: UIButton!
    @IBOutlet weak var namelabel: UILabel!
    @IBOutlet weak var descriptionlabel: UILabel!
    @IBOutlet weak var heartratelabel: UILabel!
    @IBOutlet weak var timelabel: UILabel!
    @IBOutlet weak var pausebutton: UIButton!
    @IBOutlet weak var skipbutton: UIButton!
    @IBOutlet weak var eximage: UIImageView!
    var timer = Timer()
    var timecountdown = 0.0
    var paused = false
    var i = 0
    var ind = 0
    
    @objc func startWorkout() {
        namelabel.adjustsFontSizeToFitWidth = true
        descriptionlabel.lineBreakMode = .byWordWrapping
        descriptionlabel.numberOfLines = 0
        
        //TODO: startworkout API call
        //startworkoutapi()
        
        doexercise(index: 0)
        
    }
    
    @objc func initSpotify () {
        let userDefaults = UserDefaults.standard

        if let sessionObj:AnyObject = userDefaults.object(forKey: "SpotifySession") as AnyObject? {

            let sessionDataObj = sessionObj as! Data
            let firstTimeSession = NSKeyedUnarchiver.unarchiveObject(with: sessionDataObj) as! SPTSession

            self.session = firstTimeSession
            initializePlayer(authSession: session)
        }
    }

    func initializePlayer(authSession:SPTSession){
        if self.player == nil {
            self.player = SPTAudioStreamingController.sharedInstance()
            self.player!.playbackDelegate = self
            self.player!.delegate = self
            try! player?.start(withClientId: auth.clientID)
            self.player!.login(withAccessToken: authSession.accessToken)

        }
    }
    
    func startPlayback() {
        // TODO - change to first exercise uri
        print("attempting playback")
        heartratelabel.text =  "Song: " + exercisetracknames[0][0]
        self.player?.playSpotifyURI(self.exercisetrackuris[0][0], startingWith: 0, startingWithPosition: 0, callback: { (error) in
            if (error == nil) {
                print("playing!")
            }
            if(error != nil) {
                print("error playing")
            }
        })
    }
    
    func audioStreamingDidLogin(_ audioStreaming: SPTAudioStreamingController!) {
        startPlayback()
    }
    
    func audioStreamingDidPopQueue(_ audioStreaming: SPTAudioStreamingController!) {
        ind += 1
        heartratelabel.text =  "Song: " + exercisetracknames[0][ind]
    }
    
    func audioStreaming(_ audioStreaming: SPTAudioStreamingController!, didChangePlaybackStatus isPlaying: Bool) {
        // TODO - change to queue all songs
        if(!queued) {
            if(exercisetrackuris[0].count > 1) {
                for index in 1...exercisetrackuris[0].count-1 {
                    self.player?.queueSpotifyURI(exercisetrackuris[0][index], callback: {(error) in
                        if (error == nil) {
                            print("queued!")
                        } else {
                            print("error queueing")
                        }
                    })
                    }
                self.queued = true
            }
        }
    }
    
    struct jsonRequest: Codable {
        var Result: String
        var Status: String
    }
    
    @objc func startworkoutapi() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/startworkout/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "userid=" + global.userid + "&workout=" + workoutjson +  "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                print(json)
            }
            
        }.resume()
    }
    
    @objc func doexercise(index: Int) {
        if(index == 0) {
            //startPlayback()
        }
        
        let dur = exercisedurations[index]
        namelabel.text = exercisenames[index]
        descriptionlabel.text = exercisedescriptions[index]
        timelabel.text = "Time Remaining: " + String(dur) + "s"
        let url = URL(string: exerciseimages[index])
        let data = try? Data(contentsOf: url!)
        eximage.image = UIImage(data: data!)
        eximage.contentMode = UIViewContentMode.scaleAspectFit
        
        timecountdown = Double(dur)
        timer = Timer.scheduledTimer(timeInterval: 0.1, target: self, selector: #selector(self.updateTimer), userInfo: nil, repeats: true)
        
    }
    
    @objc func updateTimer() {
        timecountdown -= 0.1
        timecountdown = ceil(timecountdown*10)/10
        timelabel.text = "Time Remaining: " + timecountdown.description + "s"
        //heartratelabel.text = "Heartrate: " + String(heartrate)
        if (timecountdown <= 0) {
            completeExercise()
        }
    }
    
    @objc func completeExercise() {
        timer.invalidate()
        timelabel.text = "Time Remaining: 0s"
        if (i < exercisenames.count-1) {
            i += 1
            doexercise(index: i)
        }
        else {
            // self.performSegue(withIdentifier: "completeSegue", sender: self)
            // exit(0)
            let storyboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
            present(vc, animated: true, completion: nil)
        }
    }
    
    @IBAction func pauseclick(_ sender: Any) {
        if (!paused) {
            paused = true
            pausebutton.setTitle("PLAY", for: .normal)
            timer.invalidate()
            self.player?.setIsPlaying(false, callback: nil)
//            do {
//                try self.player?.stop()
//            } catch {
//                print("error occurred")
//            }
        }
        else {
            paused = false
            pausebutton.setTitle("PAUSE", for: .normal)
            self.player?.setIsPlaying(true, callback: nil)
            timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.updateTimer), userInfo: nil, repeats: true)
        }
    }
    
    @IBAction func skipclick(_ sender: Any) {
        completeExercise()
    }
    
    @IBAction func quitclick(_ sender: Any) {
        exit(0)
    }
}
