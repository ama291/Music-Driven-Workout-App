//
//  WorkExerciseViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class WorkExerciseViewController: UIViewController {
    
    var userid: String!
    var workoutjson: String!
    
    //variables to be taken from workout summary
    var exercisenames: [String]!
    var exercisedescriptions: [String]!
    var exercisedurations: [Int]!
    var exerciseimages: [String]!
    
    var heartrate = 0
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
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
        vc.userid = userid!
        present(vc, animated: false, completion: nil)
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
    
    @objc func startWorkout() {
        namelabel.adjustsFontSizeToFitWidth = true
        descriptionlabel.lineBreakMode = .byWordWrapping
        descriptionlabel.numberOfLines = 0
        
        //TODO: startworkout API call
        //startworkoutapi()
        
        doexercise(index: 0)
    }
    
    struct jsonRequest: Codable {
        var Result: String
        var Status: String
    }
    
    @objc func startworkoutapi() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/startworkout/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "userid=" + userid + "&workout=" + workoutjson +  "&key=SoftCon2018"
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
        if (!paused) {
            timecountdown -= 0.1
            timecountdown = ceil(timecountdown*10)/10
            timelabel.text = "Time Remaining: " + timecountdown.description + "s"
            heartratelabel.text = "Heartrate: " + String(heartrate)
            if (timecountdown <= 0) {
                completeExercise()
            }
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
            self.performSegue(withIdentifier: "completeSegue", sender: self)
        }
    }
    
    @IBAction func pauseclick(_ sender: Any) {
        if (!paused) {
            paused = true
            pausebutton.setTitle("PLAY", for: .normal)
        }
        else {
            paused = false
            pausebutton.setTitle("PAUSE", for: .normal)
        }
    }
    
    @IBAction func skipclick(_ sender: Any) {
        completeExercise()
    }
    
}
