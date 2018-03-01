//
//  FTExerciseViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit
import CoreMotion

class FTExerciseViewController: UIViewController {

    var motionManager = CMMotionManager()
    var motionData: [[String : Double]] = []
    var timer = Timer()
    var frequency = ""
    var time = 600
    var exerciseInfo: [String:Any] = [String:Any]()
    var exercisesRemaining: [[String:Any]] = [[String:Any]]()
    var exerciseName: String!
    var numExercises: Int?
    var exerciseNum: Int?
    var isCalibration: Bool!
    var userid: String?
    
    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var frequencyLabel: UILabel!
    @IBOutlet weak var exName: UILabel!

    override func viewDidLoad() {
        super.viewDidLoad()
        self.exName.text = self.exerciseName
        self.getMotionData()
        // Do any additional setup after loading the view.
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
    
    func getMotionData() {
        self.statusLabel.text = "Do the exercise."
        // saving acceleration every 0.1 seconds
        timer = Timer.scheduledTimer(timeInterval: 60, target: self, selector: #selector(AccelerometerViewController.displayResult), userInfo: nil, repeats: false)
        
        var dispTime = -0.1;
        motionManager.accelerometerUpdateInterval = 0.1
        motionManager.startAccelerometerUpdates(to: OperationQueue.current!) {(data, error) in
            if let myData = data
            {
                self.time -= 1
                self.frequencyLabel.text = String(self.time / 10) + " seconds left"
                dispTime += 0.1
                var myDict: [String: Double] = [:]
                myDict = ["xAccl": myData.acceleration.x, "yAccl": myData.acceleration.y, "zAccl": myData.acceleration.z, "timestamp": myData.timestamp]
                
                self.motionData.append(myDict)
            }
        }
    }
    
    //json request struct
    struct jsonRequest: Codable {
        var Result: Float
        var Status: String
    }
    
    @objc func displayResult() {
        motionManager.stopAccelerometerUpdates()
        self.statusLabel.text = "complete"
        let encoder = JSONEncoder()
        encoder.outputFormatting = .prettyPrinted
        let decoder = JSONDecoder()
        do {
            let data = try? JSONSerialization.data(withJSONObject: self.motionData, options: .prettyPrinted)
            let json = String(data: data!, encoding: .utf8)
            if let json = json { // converting to a string
                let url = URL(string: "http://138.197.49.155:8000/api/fitness/accel/")!
                var request = URLRequest(url: url)
                request.httpMethod = "POST"
                let postString = "data=" + json + "&key=SoftCon2018"
                request.httpBody = postString.data(using: String.Encoding.utf8)
                let config = URLSessionConfiguration.default
                let session = URLSession(configuration: config)
                let task = session.dataTask(with: request) { (responseData, response, responseError) in
                    guard responseError == nil else {
                        return
                    }
                    if let data = responseData {
                        do {
                            let jsonResponse = try decoder.decode(jsonRequest.self, from: data)
                            self.frequency = String(describing: jsonResponse.Result)
                        }
                        catch {
                            return
                        }
                    } else {
                        return
                    }
                }
                task.resume()
            }
        }
    }
    
    @objc func updateLabel() {
        //need to fix this to callback
        self.frequencyLabel.text = self.frequency
    }
    
    @IBAction func go_to_home(_ sender: Any) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
        
    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.destination is FTCompleteViewController
        {
            let vc = segue.destination as? FTCompleteViewController
            //data to send
            vc?.exerciseName = self.exerciseName
            vc?.isCalibration = self.isCalibration
        }
        else if segue.destination is FTCheckpointViewController
        {
            let vc = segue.destination as? FTCheckpointViewController
            vc?.exerciseInfo = self.exerciseInfo
            vc?.exercisesRemaining = self.exercisesRemaining
            vc?.isCalibration = self.isCalibration
        }
    }
    
}


