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
    
    //variables to be taken from workout summary
    var exercisenames: [String]!
    var exercisedescriptions: [String]!
    var exercisedurations: [Int]!
    var exerciseimages: [String]!
    
    var heartrate = 0
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        startWorkouts()

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
    
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
    
    @objc func startWorkouts() {
        namelabel.adjustsFontSizeToFitWidth = true
        descriptionlabel.lineBreakMode = .byWordWrapping
        descriptionlabel.numberOfLines = 0
        //test values
        exercisenames = ["Lying Face Down Plate Neck Resistance", "Lying Face Up Plate Neck Resistance"]
        exercisedescriptions = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "Lorem ipsum dolor sit amet, consectetur adipiscing elit."]
        exercisedurations = [30, 30]
        exerciseimages = ["https://www.bodybuilding.com/exercises/exerciseImages/sequences/25/Male/m/25_2.jpg","https://www.bodybuilding.com/exercises/exerciseImages/sequences/26/Male/m/26_1.jpg"]
        
        doexercise(index: 0)
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
    
    //TODO: add listener for this to UI
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
    
    //TODO: add listener for this to UI, segue manually
    @IBAction func skipclick(_ sender: Any) {
        completeExercise()
    }
    
}
