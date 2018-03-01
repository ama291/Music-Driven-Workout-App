//
//  FTExDescViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//
import UIKit

class FTExDescViewController: UIViewController {
    
    var userid: Int?
    var exercisesRemaining = [[String:Any]]()
    var exerciseInfo = [String: Any]()
    var isCalibration: Bool!
    var numExercises: Int?
    var exerciseNum: Int?
    
    @IBOutlet weak var exName: UILabel!
    @IBOutlet weak var fastornormal: UILabel!
    @IBOutlet weak var workoutImage: UIImageView!
    @IBOutlet weak var exDesc: UILabel!
    @IBOutlet weak var doEx: UIButton!
    

    override func viewDidLoad() {
        super.viewDidLoad()
        print("in description")
        print(exerciseInfo)
        self.exName.text = (self.exerciseInfo["name"]! as? String)!
        if (self.isCalibration) {
            self.fastornormal.text = "Please do this exercise at workout pace for 60 seconds."
        } else {
            self.fastornormal.text = "Please do this exercise as fast as possible."
        }
        self.getWorkoutImage(workoutUrl: (self.exerciseInfo["images"]! as? String)!)
        self.exDesc.text = self.exerciseInfo["guide"]! as? String
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    func getWorkoutImage(workoutUrl: String){
        let workoutPictureURL = URL(string: workoutUrl)!
        let session = URLSession(configuration: .default)
        
        let downloadPic = session.dataTask(with: workoutPictureURL) { (data, response, error) in
            // The download has finished.
            if let e = error {
                print("The error war \(e)")
            } else {
                if let res = response as? HTTPURLResponse {
                    print("The response code was \(res.statusCode)")
                    if data != nil {
                        DispatchQueue.main.async {
                            self.workoutImage.image = UIImage(data: data!)
                        }
                    } else {
                        print("Couldn't get image: Image DNE")
                    }
                } else {
                    print("No response code; something horrible happened.")
                }
            }
        }
        downloadPic.resume()
        
    }
    
    // MARK: - Navigation
    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.destination is FTExerciseViewController
        {
            let vc = segue.destination as? FTExerciseViewController
            //data to send
            vc?.exerciseName = (self.exerciseInfo["name"]! as? String)!
            vc?.numExercises = self.numExercises
            vc?.isCalibration = self.isCalibration
            vc?.exerciseInfo = self.exerciseInfo
            vc?.exercisesRemaining = self.exercisesRemaining
        }
    }
 
}

