//
//  FTCheckpointViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class FTCheckpointViewController: UIViewController {
    
    var userid: Int?
    var exid: Int!
    var frequency: Float!
    var isTracked: Bool!
    var reply: String!
    var exerciseInfo: [String:Any] = [String:Any]()
    var exercisesRemaining: [[String:Any]] = [[String:Any]]()
    var numExercises: Int?
    var isCalibration: Bool?
    var frequencies: [[String:Any]]!
    let request = APIRequest()

    
    var exercise: [String:Any] = [String:Any]()
    @IBOutlet weak var trackButton: UIButton!
    @IBAction func track(_ sender: UIButton) {
        print("track pressed")
    }
    
    @IBOutlet weak var rateLabel: UILabel!
    @IBOutlet weak var nextExercise: UIButton!
    
    override func viewDidLoad() {
        
        super.viewDidLoad()
        frequency = 90.5
        print(self.frequencies)
        let freqDict = ["frequency":self.frequency!,"name":self.exerciseInfo["name"]]
        self.frequencies.append(freqDict)
        print(self.frequencies)
        rateLabel.text = "\(String(Int(frequency))) RPM"
        
        userid = 1 // fix later
        exid = self.exerciseInfo["id"] as! Int
        let qstr = "userid=\(String(describing: userid!))&exid=\(exid!)&key=SoftCon2018"
        request.submitPostLocal(route: "/api/fitness/istracked/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = self.request.parseJsonInitial(data: data!)!
            if self.reply == "true" {
                self.isTracked = true
            }
            else if self.reply == "false" {
                self.isTracked = false
            }
            let trackedText = !self.isTracked ? "Track Exercise" : "Un-track Exercise"
            let nextText = self.exercisesRemaining.count > 0 ? "Next Exercise" : "Finish"
            DispatchQueue.main.async {
                self.trackButton.setTitle(trackedText, for: .normal)
                self.nextExercise.setTitle(nextText, for: .normal)
            }
            
            }.resume()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    func comp(data: Data?, response: URLResponse?, error: Error?) -> Void {
        return
    }
    
    @IBAction func trackExercise(_ sender: UIButton) {
        
        let qstr = "userid=\(String(describing: userid!))&exid=\(exid!)&key=SoftCon2018"
        self.request.submitPostLocal(route: "/api/fitness/toggletracked/", qstring: qstr, completion: comp).resume()
        self.request.submitPostLocal(route: "/api/fitness/toggletracked/", qstring: qstr, completion: comp).resume()
    }
    
    
    @IBAction func next(_ sender: Any) {
        if exercisesRemaining.count > 0 {
            self.exerciseInfo = self.exercisesRemaining.remove(at: 0)
            self.performSegue(withIdentifier: "nextExercise", sender: sender)
        }
        else {
            self.performSegue(withIdentifier: "finish", sender: sender)
        }
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.destination is FTExDescViewController
        {
            let vc = segue.destination as? FTExDescViewController
            //data to send
            vc?.numExercises = self.numExercises
            vc?.isCalibration = self.isCalibration
            vc?.exerciseInfo = self.exerciseInfo
            vc?.exercisesRemaining = self.exercisesRemaining
            vc?.frequencies = self.frequencies
        }
        if segue.destination is FTCompleteViewController
        {
            let vc = segue.destination as? FTCompleteViewController
            vc?.frequencies = self.frequencies
        }
    }
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
