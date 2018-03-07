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
    var exercisedurations: [Double]!
    var exerciseimages: [String]!
    var exercisetracknames: [[String]]!
    var exercisetrackuris: [[String]]!
    var exerciseEquipment: [String]!
    var exerciseRPM: [Int]!
    var workoutid: String!
    var session:SPTSession!
    var player: SPTAudioStreamingController?
    var queued = false
    var skipping = false
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        heartratelabel.adjustsFontSizeToFitWidth = true
        descriptionlabel.adjustsFontSizeToFitWidth = true
        namelabel.adjustsFontSizeToFitWidth = true
        initSpotify()
        startWorkout()
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
    var timecountdown:Double = 0
    var paused = false
    var i = 0 // exercise index
    var ind = 0 // song index within current exercise
    
    @objc func startWorkout() {
        descriptionlabel.lineBreakMode = .byWordWrapping
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
        var descText = "Equipment: " + exerciseEquipment[self.i] + ", "
        descText += "RPM: " + String(exerciseRPM[self.i])
        descriptionlabel.text = descText
        heartratelabel.text =  "Song: " + exercisetracknames[self.i][0]
        
        
        self.player?.playSpotifyURI(self.exercisetrackuris[self.i][0], startingWith: 0, startingWithPosition: 0, callback: { (error) in
            if (error == nil) {
                //print("playing!")
            }
            if(error != nil) {
                //print("error playing")
            }
        })
    }
    
    func audioStreamingDidLogin(_ audioStreaming: SPTAudioStreamingController!) {
        startPlayback()
    }
    
    func audioStreaming(_ audioStreaming: SPTAudioStreamingController!, didStartPlayingTrack trackUri: String!) {
        heartratelabel.text =  "Song: " + exercisetracknames[self.i][self.ind]
        self.ind += 1
        if (self.ind < exercisetrackuris[self.i].count) {
            self.player?.queueSpotifyURI(exercisetrackuris[self.i][self.ind], callback: {(error) in
                if (error == nil) {
                    //print("queued!")
                 } else {
                    //print("error queueing")
                }
            })
        }
        
    }
    
    func audioStreamingDidSkip(toNextTrack audioStreaming: SPTAudioStreamingController!) {
        self.ind = 0
        startPlayback()
    }
    
    func spotifyLogout() {
        self.player?.logout()
        self.session = nil
    }
    
    struct jsonRequest: Codable {
        var Result: String
        var Status: String
    }
    
    @objc func startworkoutapi() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/startworkout/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "userid=" + global.userid + "&workout=" + self.workoutjson +  "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                //print(json)
            }
            
        }.resume()
    }
    
    @objc func pauseworkoutapi() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/pauseworkout/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString1 = "userid=" + global.userid + "&workoutid=" + self.workoutid
        let postString2 = "&paused=" + self.i.description + "&key=SoftCon2018"
        let postString = postString1 + postString2
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                //print(json)
            }
            
            }.resume()
    }
    
    
    @objc func quitworkoutapi() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/quitworkout/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "userid=" + global.userid + "&workoutid=" + workoutid +  "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                //print(json)
            }
            
            }.resume()
    }
    
    @objc func doexercise(index: Int) {
        
        let dur = exercisedurations[index]
        namelabel.text = exercisenames[index]
        timelabel.text = "Time: " + getFormattedTime(seconds: Int(dur))
        let url = URL(string: exerciseimages[index])
        let data = try? Data(contentsOf: url!)
        eximage.image = UIImage(data: data!)
        eximage.contentMode = UIViewContentMode.scaleAspectFit
        
        timecountdown = dur
        timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.updateTimer), userInfo: nil, repeats: true)
        
    }
    
    func getFormattedTime(seconds: Int) -> String {
        let formatter = DateComponentsFormatter()
        formatter.allowedUnits = [.minute, .second]
        formatter.unitsStyle = .full
        return formatter.string(from: TimeInterval(seconds))!
    }
    
    @objc func updateTimer() {
        timecountdown -= 1
        timelabel.text = "Time: " + getFormattedTime(seconds: Int(timecountdown))
        if (timecountdown <= 0) {
            completeExercise()
        }
    }
    
    @objc func completeExercise() {
        timer.invalidate()
        timelabel.text = "Time: 0 minutes 0 seconds"
        if (i < exercisenames.count-1) {
            i += 1
            doexercise(index: i)
            self.player?.skipNext({ (error) in
                if (error == nil) {
                    //print("skipped!")
                }
                if(error != nil) {
                    //print("error skipping")
                }
            })
        }
        else {
            self.player?.setIsPlaying(false, callback: nil)
            spotifyLogout()
            let storyboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
            global.completedWorkout = true
            present(vc, animated: true, completion: nil)
        }
    }
    
    @IBAction func pauseclick(_ sender: Any) {
        if (!paused) {
            paused = true
            pausebutton.setTitle("PLAY", for: .normal)
            timer.invalidate()
            self.player?.setIsPlaying(false, callback: nil)
        }
        else {
            paused = false
            pausebutton.setTitle("PAUSE", for: .normal)
            timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.updateTimer), userInfo: nil, repeats: true)
            self.player?.setIsPlaying(true, callback: nil)
        }
    }
    
    @IBAction func skipclick(_ sender: Any) {
        if(!paused) {
            completeExercise()
        }
    }
    
    @IBAction func quitclick(_ sender: Any) {
        self.player?.setIsPlaying(false, callback: nil)
        spotifyLogout()
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        global.completedWorkout = true
        present(vc, animated: true, completion: nil)
    }
}

