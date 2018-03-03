//
//  ThemesMenuViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class ThemesMenuViewController: UIViewController {

    var userid: String!
    var themes: [[String:Any]]!
    var selectedTheme: [String:Any]!
    
    var viewModel = ThemeViewModel()
    var request = APIRequest()
    
    @IBOutlet weak var viewButton: UIButton!
    @IBAction func switchThemes(_ sender: Any) {

    }
    @IBOutlet weak var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.themes = [["theme":"theme", "name": "theme name", "spotifyId": "Spotify id", "numworkouts": "4"], ["theme":"theme 2", "name": "theme name 2", "spotifyId": "Spotify id 2", "numworkouts": "6"]]
        
        let vmitems = self.themes!.map { ThemeViewModelItem(item: ThemeModel(title: "\($0["name"]! as! String)" , data: $0)) }

        print(vmitems[0].title)
        
        self.viewModel.setItems(items: vmitems)

        self.tableView?.register(ThemeCustomCell.nib, forCellReuseIdentifier: ThemeCustomCell.identifier)
        self.tableView?.dataSource = self.viewModel
        self.tableView?.delegate = self.viewModel
        self.tableView?.estimatedRowHeight = 100
        self.tableView?.rowHeight = UITableViewAutomaticDimension
        self.tableView?.allowsSelection = true
        self.tableView?.separatorStyle = .none
        
        viewModel.didToggleSelection = { [weak self] hasSelection in
            let selected = self!.viewModel.selectedItems
            if selected.count == 0 {
                return
            }
            self!.selectedTheme = self!.viewModel.selectedItems.map{ $0.data}[0]
            self!.performSegue(withIdentifier: "toTheme", sender: nil)
        }
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.destination is ThemeViewController
        {
            let vc = segue.destination as? ThemeViewController
            //data to send
            vc?.userid = userid
            vc?.selectedTheme = self.selectedTheme
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
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    
}
